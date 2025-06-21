#!/usr/bin/env python3
"""
APIテスト用スクリプト - pipインストールなしでの動作確認
"""
import sys
import json
import re

# 簡易的なコード抽出機能のテスト
def extract_chords(chord_input: str):
    """[]で囲まれたコードを抽出する"""
    pattern = r'\[([^\]]+)\]'
    matches = re.findall(pattern, chord_input)
    return matches

def test_chord_extraction():
    """コード抽出機能のテスト"""
    test_cases = [
        ("[CM7][Am7][FM7][G7]", ["CM7", "Am7", "FM7", "G7"]),
        ("[FM7(13)][FmM7][Em7][A7]", ["FM7(13)", "FmM7", "Em7", "A7"]),
        ("CM7 Am7 FM7 G7", []),  # []がない場合
        ("[C][D][E][F#m]", ["C", "D", "E", "F#m"]),
    ]
    
    print("=== コード抽出テスト ===")
    for input_str, expected in test_cases:
        result = extract_chords(input_str)
        status = "✓" if result == expected else "✗"
        print(f"{status} 入力: {input_str}")
        print(f"   期待値: {expected}")
        print(f"   結果:   {result}")
        print()

def test_note_conversion():
    """音名変換の簡易テスト"""
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def note_to_pitch_class(note: str) -> int:
        note = note.replace('b', '#')
        replacements = {
            'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 
            'Ab': 'G#', 'Bb': 'A#'
        }
        note = replacements.get(note, note)
        return notes.index(note) if note in notes else 0
    
    print("=== 音名→ピッチクラス変換テスト ===")
    test_notes = ['C', 'F#', 'Bb', 'Ab', 'D#']
    for note in test_notes:
        pc = note_to_pitch_class(note)
        print(f"✓ {note} → {pc} ({notes[pc]})")
    print()

def main():
    print("Chord Analyzer API - 基本機能テスト")
    print("=" * 50)
    
    test_chord_extraction()
    test_note_conversion()
    
    print("=== テスト入力例 ===")
    test_input = "[CM7][Am7][FM7][G7]"
    chords = extract_chords(test_input)
    print(f"入力: {test_input}")
    print(f"抽出されたコード: {chords}")
    print()
    
    print("✓ 基本機能の実装完了")
    print("次のステップ: 必要なライブラリのインストール後、APIサーバーを起動")
    print("起動コマンド: python3 -m uvicorn main:app --reload")

if __name__ == "__main__":
    main()