#!/usr/bin/env python3
"""
Debug Em7 degree display issue: vii7 vs viim7
"""

def debug_em7_issue():
    print("=== Em7 度数表示問題の調査 ===\n")
    
    # 現在のロジックをシミュレート
    def note_to_pc(note: str) -> int:
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        normalized = note.replace('Db', 'C#').replace('Eb', 'D#').replace('Gb', 'F#').replace('Ab', 'G#').replace('Bb', 'A#')
        return notes.index(normalized) if normalized in notes else -1
    
    def get_chord_root(chord: str) -> str:
        import re
        match = re.match(r'^([A-G][#b]?)', chord)
        return match.group(1) if match else ''
    
    def get_chord_type(chord: str):
        root = get_chord_root(chord)
        remainder = chord[len(root):]
        
        import re
        if re.match(r'^m(?!aj)', remainder):
            extensions = remainder[1:]
            return {'quality': 'minor', 'extensions': extensions}
        elif re.match(r'^(dim|°)', remainder):
            extensions = re.sub(r'^(dim|°)', '', remainder)
            return {'quality': 'diminished', 'extensions': extensions}
        elif re.match(r'^(aug|\+)', remainder):
            extensions = re.sub(r'^(aug|\+)', '', remainder)
            return {'quality': 'augmented', 'extensions': extensions}
        else:
            return {'quality': 'major', 'extensions': remainder}
    
    def analyze_em7():
        chord = 'Em7'
        main_key = 'C Major'
        
        print(f"コード: {chord}")
        print(f"キー: {main_key}")
        
        # コードタイプ分析
        chord_type = get_chord_type(chord)
        print(f"検出されたコードタイプ: {chord_type}")
        
        # 度数計算
        key_root = 'C'
        chord_root = get_chord_root(chord)
        
        key_pc = note_to_pc(key_root)
        chord_pc = note_to_pc(chord_root)
        
        interval = (chord_pc - key_pc + 12) % 12
        
        print(f"コードルート: {chord_root} (PC: {chord_pc})")
        print(f"キールート: {key_root} (PC: {key_pc})")
        print(f"インターバル: {interval}")
        
        # 度数マッピング
        major_degrees = ['I', 'bII', 'II', 'bIII', 'III', 'IV', '#IV', 'V', 'bVI', 'VI', 'bVII', 'VII']
        base_degree = major_degrees[interval]
        
        print(f"ベース度数: {base_degree}")
        print(f"コード性質: {chord_type['quality']}")
        print(f"エクステンション: '{chord_type['extensions']}'")
        
        # 現在のロジック
        if chord_type['quality'] == 'minor':
            base_degree = base_degree.lower()
        
        result = base_degree + chord_type['extensions']
        
        print(f"現在の結果: {result}")
        print(f"期待される結果: viim7")
        
        # 問題の特定
        print(f"\n問題分析:")
        print(f"- Em7のコードタイプ: {chord_type}")
        print(f"- マイナーコードとして認識されているか: {chord_type['quality'] == 'minor'}")
        print(f"- extensions: '{chord_type['extensions']}'")
        print(f"- base_degree.lower(): '{base_degree.lower()}'")
        
        if chord_type['quality'] == 'minor' and chord_type['extensions'] == '7':
            print(f"- 正しい結果: {base_degree.lower()}m{chord_type['extensions']}")
        
    analyze_em7()

if __name__ == "__main__":
    debug_em7_issue()