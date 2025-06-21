#!/usr/bin/env python3
"""
Phase 2デバッグ: 借用元候補が表示されない問題の調査
"""
import requests
import json

def debug_api_response():
    base_url = "http://localhost:8000"
    
    print("=== Phase 2 API レスポンス詳細デバッグ ===")
    
    test_input = "[C][Am][Fm][G]"
    payload = {"chord_input": test_input}
    
    try:
        response = requests.post(f"{base_url}/analyze", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"入力: {test_input}")
            print(f"推定キー: {result['main_key']}")
            print(f"借用和音数: {len(result['borrowed_chords'])}")
            
            print(f"\n完全なレスポンス:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 各借用和音の詳細分析
            for i, borrowed in enumerate(result['borrowed_chords']):
                print(f"\n借用和音 {i+1}: {borrowed['chord']}")
                print(f"非ダイアトニック音: {borrowed['non_diatonic_notes']}")
                print(f"候補数: {len(borrowed['source_candidates'])}")
                
                for j, candidate in enumerate(borrowed['source_candidates']):
                    print(f"  候補{j+1}: {candidate}")
                    
        else:
            print(f"エラー: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"例外エラー: {e}")

def debug_local_functions():
    """ローカル関数の動作確認"""
    print(f"\n=== ローカル関数デバッグ ===")
    
    # 必要な定義をインポート
    import sys
    sys.path.append('.')
    
    # main.pyから関数をインポートして直接テスト
    try:
        from main import (
            get_diatonic_notes, 
            detect_non_diatonic_notes,
            find_borrowed_sources,
            get_chord_components,
            extract_chords
        )
        
        test_input = "[C][Am][Fm][G]"
        main_key = "C Major"
        
        print(f"1. コード抽出:")
        chords = extract_chords(test_input)
        print(f"   {chords}")
        
        print(f"\n2. ダイアトニック音:")
        diatonic_notes = get_diatonic_notes(main_key)
        print(f"   {main_key}: {diatonic_notes}")
        
        print(f"\n3. 各コードの構成音:")
        for chord in chords:
            components = get_chord_components(chord)
            print(f"   {chord}: {components}")
        
        print(f"\n4. 非ダイアトニック音検出:")
        non_diatonic = detect_non_diatonic_notes(chords, main_key)
        print(f"   {non_diatonic}")
        
        print(f"\n5. 借用元候補:")
        if non_diatonic:
            borrowed = find_borrowed_sources(non_diatonic, main_key)
            for b in borrowed:
                print(f"   {b.chord}: {len(b.source_candidates)} 候補")
                for candidate in b.source_candidates[:2]:  # 上位2つだけ
                    print(f"     - {candidate.key} ({candidate.relationship}) {candidate.confidence:.3f}")
        
    except ImportError as e:
        print(f"インポートエラー: {e}")
    except Exception as e:
        print(f"実行エラー: {e}")

if __name__ == "__main__":
    debug_api_response()
    debug_local_functions()