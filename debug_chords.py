#!/usr/bin/env python3
"""
pychordライブラリの動作確認
"""
from pychord import Chord
import re

def test_pychord():
    print("=== pychord動作テスト ===")
    
    test_chords = ["CM7", "Am7", "FM7", "G7", "FmM7", "Em7", "A7"]
    
    for chord_symbol in test_chords:
        try:
            chord = Chord(chord_symbol)
            components = chord.components()
            notes = [note.name for note in components]
            print(f"{chord_symbol}: {notes}")
        except Exception as e:
            print(f"{chord_symbol}: エラー - {e}")
    
    print("\n=== コード抽出テスト ===")
    test_input = "[CM7][Am7][FM7][G7]"
    pattern = r'\[([^\]]+)\]'
    matches = re.findall(pattern, test_input)
    print(f"入力: {test_input}")
    print(f"抽出結果: {matches}")
    
    print("\n=== 実際のAPIロジックテスト ===")
    chords = matches
    
    # ピッチクラスベクトル作成のテスト
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def note_to_pitch_class(note: str) -> int:
        note = note.replace('b', '#')  
        if note == 'Db': note = 'C#'
        elif note == 'Eb': note = 'D#' 
        elif note == 'Gb': note = 'F#'
        elif note == 'Ab': note = 'G#'
        elif note == 'Bb': note = 'A#'
        
        return NOTES.index(note) if note in NOTES else 0
    
    vector = [0] * 12
    all_notes = []
    
    for chord_symbol in chords:
        try:
            chord = Chord(chord_symbol)
            notes = [note.name for note in chord.components()]
            all_notes.extend(notes)
            print(f"{chord_symbol} -> {notes}")
            
            for note in notes:
                pitch_class = note_to_pitch_class(note)
                vector[pitch_class] += 1
                print(f"  {note} -> pitch class {pitch_class}")
                
        except Exception as e:
            print(f"エラー処理 {chord_symbol}: {e}")
    
    print(f"\n全構成音: {all_notes}")
    print(f"ピッチクラスベクトル: {vector}")
    
    # 正規化  
    if sum(vector) > 0:
        normalized = [v / sum(vector) for v in vector]
        print(f"正規化後: {[round(v, 3) for v in normalized]}")
    else:
        print("警告: ベクトルの合計が0です")

if __name__ == "__main__":
    test_pychord()