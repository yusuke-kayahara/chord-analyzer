#!/usr/bin/env python3
"""
Phase 2: 借用和音検出機能のテスト
"""
import requests
import json

def test_borrowed_chords():
    base_url = "http://localhost:8000"
    
    print("=== Phase 2: 借用和音検出テスト ===")
    
    test_cases = [
        {
            "name": "C Major with iv chord (Fm)",
            "input": "[C][Am][Fm][G]",
            "expected_key": "C Major",
            "expected_borrowed": ["Fm"],
            "description": "CメジャーキーにおけるFm（iv度）借用和音"
        },
        {
            "name": "C Major with bVII chord (Bb)",
            "input": "[C][F][Bb][C]", 
            "expected_key": "C Major",
            "expected_borrowed": ["Bb"],
            "description": "CメジャーキーにおけるBb（bVII度）借用和音"
        },
        {
            "name": "C Major with FmM7 (parallel minor)",
            "input": "[FM7][FmM7][Em7][A7]",
            "expected_key": "C Major",
            "expected_borrowed": ["FmM7", "A7"],
            "description": "FmM7（平行短調由来）とA7（セカンダリドミナント）"
        },
        {
            "name": "A Minor with VI chord (F)",
            "input": "[Am][F][C][G]",
            "expected_key": "C Major",  # 相対長調として検出される
            "expected_borrowed": [],
            "description": "Amマイナー進行（相対長調として解釈）"
        },
        {
            "name": "Complex borrowed progression",
            "input": "[C][Ab][F][G]",
            "expected_key": "C Major", 
            "expected_borrowed": ["Ab"],
            "description": "CメジャーキーにおけるAb（bVI度）借用和音"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n【テスト{i}: {test_case['name']}】")
        print(f"説明: {test_case['description']}")
        print(f"入力: {test_case['input']}")
        
        try:
            payload = {"chord_input": test_case["input"]}
            response = requests.post(f"{base_url}/analyze", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"推定キー: {result['main_key']} (期待: {test_case['expected_key']})")
                print(f"信頼度: {result['confidence']:.3f}")
                print(f"借用和音数: {len(result['borrowed_chords'])}")
                
                # 借用和音の詳細表示
                for borrowed in result['borrowed_chords']:
                    print(f"\n  借用和音: {borrowed['chord']}")
                    print(f"  非ダイアトニック音: {borrowed['non_diatonic_notes']}")
                    print(f"  借用元候補:")
                    
                    for candidate in borrowed['source_candidates']:
                        print(f"    - {candidate['key']} ({candidate['relationship']}) 信頼度: {candidate['confidence']:.3f}")
                
                # 期待値との比較
                detected_borrowed = [b['chord'] for b in result['borrowed_chords']]
                key_match = "✅" if result['main_key'] == test_case['expected_key'] else "❌"
                borrowed_match = "✅" if set(detected_borrowed) >= set(test_case['expected_borrowed']) else "❌"
                
                print(f"\n  結果: キー推定 {key_match}, 借用和音検出 {borrowed_match}")
                
            else:
                print(f"❌ エラー: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ 例外エラー: {e}")
    
    print(f"\n{'='*60}")
    print("✅ Phase 2テスト完了")

def test_diatonic_scale():
    """ダイアトニックスケール機能の単体テスト"""
    print("\n=== ダイアトニックスケール単体テスト ===")
    
    # ローカルテスト用の簡易実装
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    MAJOR_SCALE_INTERVALS = [0, 2, 4, 5, 7, 9, 11]
    MINOR_SCALE_INTERVALS = [0, 2, 3, 5, 7, 8, 10]
    
    def note_to_pitch_class(note: str) -> int:
        return NOTES.index(note) if note in NOTES else 0
    
    def get_diatonic_notes(key: str):
        parts = key.split()
        if len(parts) != 2:
            return []
        
        root_note = parts[0]
        key_type = parts[1]
        root_pc = note_to_pitch_class(root_note)
        
        if key_type == "Major":
            intervals = MAJOR_SCALE_INTERVALS
        elif key_type == "Minor":
            intervals = MINOR_SCALE_INTERVALS
        else:
            return []
        
        diatonic_notes = []
        for interval in intervals:
            pc = (root_pc + interval) % 12
            diatonic_notes.append(NOTES[pc])
        
        return diatonic_notes
    
    test_keys = [
        ("C Major", ["C", "D", "E", "F", "G", "A", "B"]),
        ("G Major", ["G", "A", "B", "C", "D", "E", "F#"]),
        ("A Minor", ["A", "B", "C", "D", "E", "F", "G"]),
        ("F# Minor", ["F#", "G#", "A", "B", "C#", "D", "E"])
    ]
    
    for key, expected in test_keys:
        result = get_diatonic_notes(key)
        match = "✅" if result == expected else "❌"
        print(f"{match} {key}: {result}")
        if result != expected:
            print(f"   期待値: {expected}")

if __name__ == "__main__":
    print("Phase 2: 借用和音検出機能 - 総合テスト")
    print("=" * 60)
    
    # 基本機能テスト
    test_diatonic_scale()
    
    # APIテスト
    try:
        test_borrowed_chords()
    except requests.exceptions.ConnectionError:
        print("❌ APIサーバーに接続できません。サーバーが起動していることを確認してください。")
        print("起動コマンド: source venv/bin/activate && python3 -m uvicorn main:app --reload")