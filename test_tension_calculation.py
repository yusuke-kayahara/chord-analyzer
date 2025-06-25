#!/usr/bin/env python3
"""
テンション音計算の独立テスト
"""

import re

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

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
    # 基本的なインターバルマッピング（オクターブ内に正規化）
    interval_map = {
        9: 2,   # 9度 = 2度
        11: 5,  # 11度 = 4度  
        13: 9,  # 13度 = 6度
        # 基本度数も対応
        2: 2,   # 2度
        4: 5,   # 4度
        6: 9,   # 6度
        7: 10,  # 7度
    }
    
    base_interval = interval_map.get(interval, interval % 12)
    
    # 修飾記号を適用
    if modifier == '#' or modifier == '+':
        base_interval += 1
    elif modifier == 'b' or modifier == '-':
        base_interval -= 1
    
    # ルートからの音程を計算
    tension_pc = (root_pc + base_interval) % 12
    return tension_pc

def calculate_tension_notes(core_chord: str, tension_part: str) -> list:
    """テンション記法から実際のテンション音を計算"""
    tension_notes = []
    
    try:
        # コードのルート音を取得
        root_match = re.match(r'^([A-G][#b]?)', core_chord)
        if not root_match:
            return []
        
        root_note = root_match.group(1)
        root_pc = note_to_pitch_class(root_note)
        
        # テンション要素を分割
        tension_elements = re.split(r'[,、\s]+', tension_part)
        
        for element in tension_elements:
            element = element.strip()
            if not element:
                continue
                
            # テンション記法を解析 (例: #9, b13, 11)
            tension_match = re.match(r'([#b+-]?)(\d+)', element)
            if tension_match:
                modifier = tension_match.group(1) if tension_match.group(1) else ''
                number = int(tension_match.group(2))
                
                # テンション音のピッチクラスを計算
                tension_pc = calculate_tension_pitch_class(root_pc, number, modifier)
                if tension_pc is not None:
                    tension_note = NOTES[tension_pc]
                    tension_notes.append(tension_note)
    
    except Exception as e:
        print(f"Error in calculate_tension_notes: {e}")
    
    return tension_notes

def test_tension_calculation():
    print("=== テンション音計算テスト ===\\n")
    
    test_cases = [
        ("C", "#9"),    # C(#9) → C + D#
        ("C", "b9"),    # C(b9) → C + Db  
        ("C", "11"),    # C(11) → C + F
        ("C", "#11"),   # C(#11) → C + F#
        ("C", "13"),    # C(13) → C + A
        ("C", "b13"),   # C(b13) → C + Ab
        ("G", "#9"),    # G(#9) → G + A#
        ("F", "b9"),    # F(b9) → F + Gb
    ]
    
    for root, tension in test_cases:
        tension_notes = calculate_tension_notes(root, tension)
        root_pc = note_to_pitch_class(root)
        
        print(f"{root}({tension}):") 
        print(f"  ルート: {root} (PC: {root_pc})")
        print(f"  テンション音: {tension_notes}")
        
        # 手動で期待値を確認
        if tension == "#9":
            expected_pc = (root_pc + 3) % 12  # #9 = #2度 = 長2度+半音
            expected_note = NOTES[expected_pc]
            print(f"  期待値: {expected_note} (PC: {expected_pc})")
        elif tension == "b9":
            expected_pc = (root_pc + 1) % 12  # b9 = b2度 = 半音
            expected_note = NOTES[expected_pc]
            print(f"  期待値: {expected_note} (PC: {expected_pc})")
        
        print()

def test_c_sharp9_specifically():
    print("=== C(#9) 特定テスト ===\\n")
    
    # C(#9)の期待される構成音
    print("C(#9)の期待される構成音:")
    print("  C (ルート)")
    print("  E (長3度)")  
    print("  G (完全5度)")
    print("  D# (#9度)")
    print()
    
    # 実際の計算
    core_chord = "C"
    tension_part = "#9"
    
    print("実際の計算結果:")
    tension_notes = calculate_tension_notes(core_chord, tension_part)
    print(f"  コア: {core_chord}")
    print(f"  テンション: {tension_part}")
    print(f"  計算されたテンション音: {tension_notes}")
    
    # Cメジャーキーのダイアトニック音
    c_major_notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    print(f"\\nCメジャーキーのダイアトニック音: {c_major_notes}")
    
    # 非ダイアトニック音をチェック
    for note in tension_notes:
        if note not in c_major_notes:
            print(f"  → {note} は非ダイアトニック音！（借用和音となるべき）")
        else:
            print(f"  → {note} はダイアトニック音")

if __name__ == "__main__":
    test_tension_calculation()
    test_c_sharp9_specifically()