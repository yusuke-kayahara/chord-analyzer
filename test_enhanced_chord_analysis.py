#!/usr/bin/env python3
"""
テンション音を含む和音分析の包括的テスト
"""

import re

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
MAJOR_SCALE_INTERVALS = [0, 2, 4, 5, 7, 9, 11]

def normalize_note(note: str) -> str:
    """音名を正規化（異名同音を統一）"""
    replacements = {
        'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 
        'Ab': 'G#', 'Bb': 'A#'
    }
    return replacements.get(note, note)

def note_to_pitch_class(note: str) -> int:
    """音名をピッチクラス番号に変換"""
    normalized_note = normalize_note(note)
    return NOTES.index(normalized_note) if normalized_note in NOTES else 0

def calculate_tension_pitch_class(root_pc: int, interval: int, modifier: str) -> int:
    """テンション音のピッチクラスを計算"""
    interval_map = {
        9: 2, 11: 5, 13: 9,
        2: 2, 4: 5, 6: 9, 7: 10,
    }
    
    base_interval = interval_map.get(interval, interval % 12)
    
    if modifier == '#' or modifier == '+':
        base_interval += 1
    elif modifier == 'b' or modifier == '-':
        base_interval -= 1
    
    tension_pc = (root_pc + base_interval) % 12
    return tension_pc

def calculate_tension_notes(core_chord: str, tension_part: str) -> list:
    """テンション記法から実際のテンション音を計算"""
    tension_notes = []
    
    try:
        root_match = re.match(r'^([A-G][#b]?)', core_chord)
        if not root_match:
            return []
        
        root_note = root_match.group(1)
        root_pc = note_to_pitch_class(root_note)
        
        tension_elements = re.split(r'[,、\s]+', tension_part)
        
        for element in tension_elements:
            element = element.strip()
            if not element:
                continue
                
            tension_match = re.match(r'([#b+-]?)(\d+)', element)
            if tension_match:
                modifier = tension_match.group(1) if tension_match.group(1) else ''
                number = int(tension_match.group(2))
                
                tension_pc = calculate_tension_pitch_class(root_pc, number, modifier)
                if tension_pc is not None:
                    tension_note = NOTES[tension_pc]
                    tension_notes.append(tension_note)
    
    except Exception as e:
        print(f"Error: {e}")
    
    return tension_notes

def get_chord_components_enhanced(chord_symbol: str) -> list:
    """テンション音を含むコード構成音を取得（pychord代替）"""
    # 簡単なコード解析（基本的なコードのみ）
    try:
        # テンション付きコードの処理
        tension_match = re.match(r'^([A-G][#b]?(?:maj|m|dim|aug|sus[24]?)?(?:7|maj7|mM7|M7)?)\(([^)]+)\)', chord_symbol)
        
        if tension_match:
            core_chord_str = tension_match.group(1)
            tension_part = tension_match.group(2)
            
            # コア部分の構成音を取得（簡易版）
            base_components = get_basic_chord_components(core_chord_str)
            
            # テンション音を計算して追加
            tension_notes = calculate_tension_notes(core_chord_str, tension_part)
            
            # 重複を除去して結合
            all_components = list(set(base_components + tension_notes))
            return all_components
        else:
            # テンション記法がない場合
            return get_basic_chord_components(chord_symbol)
            
    except Exception:
        return []

def get_basic_chord_components(chord_symbol: str) -> list:
    """基本的なコード構成音を取得（簡易版）"""
    # 簡易的なコード解析
    root_match = re.match(r'^([A-G][#b]?)', chord_symbol)
    if not root_match:
        return []
    
    root_note = root_match.group(1)
    root_pc = note_to_pitch_class(root_note)
    
    # 基本的なトライアド
    if 'm' in chord_symbol and 'maj' not in chord_symbol:
        # マイナーコード
        third_pc = (root_pc + 3) % 12  # 短3度
    else:
        # メジャーコード（デフォルト）
        third_pc = (root_pc + 4) % 12  # 長3度
    
    fifth_pc = (root_pc + 7) % 12  # 完全5度
    
    notes = [NOTES[root_pc], NOTES[third_pc], NOTES[fifth_pc]]
    
    # 7thコード
    if '7' in chord_symbol:
        if 'maj7' in chord_symbol or 'M7' in chord_symbol:
            seventh_pc = (root_pc + 11) % 12  # 長7度
        else:
            seventh_pc = (root_pc + 10) % 12  # 短7度
        notes.append(NOTES[seventh_pc])
    
    return notes

def get_diatonic_notes(key: str) -> list:
    """指定されたキーのダイアトニック音を取得"""
    parts = key.split()
    if len(parts) < 2:
        return []
    
    root_note = parts[0]
    key_type = parts[1]
    
    root_pc = note_to_pitch_class(root_note)
    
    if key_type == "Major":
        intervals = MAJOR_SCALE_INTERVALS
    else:
        return []  # 簡略化
    
    diatonic_notes = []
    for interval in intervals:
        pc = (root_pc + interval) % 12
        diatonic_notes.append(NOTES[pc])
    
    return diatonic_notes

def detect_non_diatonic_notes_enhanced(chord_symbol: str, main_key: str) -> dict:
    """非ダイアトニック音を含むコードを検出（改良版）"""
    diatonic_notes = get_diatonic_notes(main_key)
    chord_notes = get_chord_components_enhanced(chord_symbol)
    
    normalized_chord_notes = [normalize_note(note) for note in chord_notes]
    normalized_diatonic_notes = [normalize_note(note) for note in diatonic_notes]
    non_diatonic_notes = [note for note in chord_notes 
                         if normalize_note(note) not in normalized_diatonic_notes]
    
    return {
        'chord': chord_symbol,
        'chord_notes': chord_notes,
        'non_diatonic_notes': non_diatonic_notes,
        'is_borrowed': len(non_diatonic_notes) > 0
    }

def test_tension_chord_analysis():
    print("=== テンション和音分析テスト ===\n")
    
    main_key = "C Major"
    print(f"テストキー: {main_key}")
    print(f"ダイアトニック音: {get_diatonic_notes(main_key)}")
    print()
    
    test_chords = [
        "C",        # ダイアトニック
        "C(#9)",    # 借用和音（D#が非ダイアトニック）
        "C(b9)",    # 借用和音（C#が非ダイアトニック）
        "G7(#9)",   # 借用和音（A#が非ダイアトニック）
        "Dm7(#11)", # 借用和音（G#が非ダイアトニック）
        "F(b13)",   # 借用和音（Dbが非ダイアトニック）
        "C(9)",     # ダイアトニック（Dが含まれる）
        "G7(13)",   # ダイアトニック（Eが含まれる）
    ]
    
    for chord in test_chords:
        result = detect_non_diatonic_notes_enhanced(chord, main_key)
        status = "借用和音" if result['is_borrowed'] else "ダイアトニック"
        
        print(f"{chord:>10}: {status}")
        print(f"          構成音: {result['chord_notes']}")
        if result['non_diatonic_notes']:
            print(f"          非ダイアトニック音: {result['non_diatonic_notes']}")
        print()
    
    print("期待される結果:")
    print("✅ C(#9), C(b9), G7(#9), Dm7(#11), F(b13) → 借用和音")
    print("✅ C, C(9), G7(13) → ダイアトニック")

def test_user_reported_issue():
    print("\n=== ユーザー報告問題のテスト ===\n")
    
    print("問題: C(#9)単体でテストすると、C Majorで全部ダイアトニックと判定される")
    print("期待: #9がレ#だから借用和音と判定してほしい")
    print()
    
    chord = "C(#9)"
    key = "C Major"
    
    result = detect_non_diatonic_notes_enhanced(chord, key)
    
    print(f"コード: {chord}")
    print(f"キー: {key}")
    print(f"構成音: {result['chord_notes']}")
    print(f"非ダイアトニック音: {result['non_diatonic_notes']}")
    print(f"判定: {'借用和音' if result['is_borrowed'] else 'ダイアトニック'}")
    
    if result['is_borrowed'] and 'D#' in result['non_diatonic_notes']:
        print("\n✅ 修正成功！C(#9)が正しく借用和音として判定された")
        print("   D#（#9度）が非ダイアトニック音として検出された")
    else:
        print("\n❌ まだ問題が残っている")

if __name__ == "__main__":
    test_tension_chord_analysis()
    test_user_reported_issue()