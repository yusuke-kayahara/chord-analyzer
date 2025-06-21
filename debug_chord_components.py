#!/usr/bin/env python3
"""
pychordでのコード構成音取得のデバッグ
"""
from pychord import Chord

def debug_fm_chord():
    print("=== Fmコードの構成音詳細調査 ===")
    
    chord_symbol = "Fm"
    chord = Chord(chord_symbol)
    
    print(f"コード: {chord_symbol}")
    print(f"components(): {chord.components()}")
    print(f"root: {chord.root}")
    print(f"quality: {chord.quality}")
    
    # 期待値: ['F', 'Ab', 'C']
    # F + 短3度(Ab) + 完全5度(C)
    
    expected = ['F', 'Ab', 'C']
    actual = chord.components()
    
    print(f"期待値: {expected}")
    print(f"実際値: {actual}")
    print(f"一致: {'✅' if actual == expected else '❌'}")
    
    # 他のマイナーコードも確認
    minor_chords = ['Am', 'Dm', 'Em', 'Gm']
    for minor_chord in minor_chords:
        try:
            chord = Chord(minor_chord)
            components = chord.components()
            print(f"{minor_chord}: {components}")
        except Exception as e:
            print(f"{minor_chord}: エラー - {e}")

def debug_key_matching():
    """キーマッチング機能のデバッグ"""
    print(f"\n=== キーマッチング機能デバッグ ===")
    
    # 手動でダイアトニック音を定義
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    MAJOR_SCALE_INTERVALS = [0, 2, 4, 5, 7, 9, 11]
    MINOR_SCALE_INTERVALS = [0, 2, 3, 5, 7, 8, 10]
    
    def note_to_pitch_class(note):
        replacements = {'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'}
        note = replacements.get(note, note)
        return NOTES.index(note) if note in NOTES else 0
    
    def get_diatonic_notes(key):
        parts = key.split()
        if len(parts) != 2:
            return []
        
        root_note = parts[0]
        key_type = parts[1]
        root_pc = note_to_pitch_class(root_note)
        
        intervals = MAJOR_SCALE_INTERVALS if key_type == "Major" else MINOR_SCALE_INTERVALS
        
        diatonic_notes = []
        for interval in intervals:
            pc = (root_pc + interval) % 12
            diatonic_notes.append(NOTES[pc])
        
        return diatonic_notes
    
    # Fmの構成音 ['F', 'Ab', 'C'] をチェック
    fm_notes = ['F', 'G#', 'C']  # AbをG#として確認
    print(f"Fm構成音（G#表記）: {fm_notes}")
    
    # 各キーでFmが完全にダイアトニックかチェック
    test_keys = [
        'C Minor', 'F Minor', 'Bb Minor', 'Eb Minor',
        'Ab Major', 'Db Major', 'Gb Major'
    ]
    
    for key in test_keys:
        diatonic = get_diatonic_notes(key)
        print(f"\n{key}: {diatonic}")
        
        # Fmの各音がこのキーに含まれるかチェック
        matches = []
        for note in fm_notes:
            if note in diatonic:
                matches.append(f"✅{note}")
            else:
                matches.append(f"❌{note}")
        
        all_match = all(note in diatonic for note in fm_notes)
        print(f"  Fm適合: {matches} -> {'✅完全一致' if all_match else '❌部分一致'}")

if __name__ == "__main__":
    debug_fm_chord()
    debug_key_matching()