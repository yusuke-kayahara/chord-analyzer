#!/usr/bin/env python3
"""
C#dim(9)の借用和音判定問題をデバッグ
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_tension_borrowed_issue():
    print("=== C#dim(9) 借用和音判定問題のデバッグ ===\n")
    
    # pychordの動作をテスト
    try:
        from pychord import Chord
        
        print("1. pychordでのコード解析テスト:")
        test_chords = ['C#dim', 'C#dim(9)', 'C#°', 'C#°(9)']
        
        for chord_symbol in test_chords:
            try:
                chord = Chord(chord_symbol)
                components = chord.components()
                print(f"   {chord_symbol:>10} → {components}")
            except Exception as e:
                print(f"   {chord_symbol:>10} → エラー: {e}")
        
        print()
        
    except ImportError:
        print("pychordがインストールされていません")
        return
    
    # 借用和音検出ロジックのシミュレーション
    print("2. 借用和音検出ロジックのシミュレーション:")
    
    def get_diatonic_notes(key: str):
        """Gメジャーキーのダイアトニック音"""
        if key == "G Major":
            return ['G', 'A', 'B', 'C', 'D', 'E', 'F#']
        return []
    
    def normalize_note(note: str) -> str:
        replacements = {
            'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 
            'Ab': 'G#', 'Bb': 'A#'
        }
        return replacements.get(note, note)
    
    def check_borrowed_chord(chord_symbol: str, main_key: str):
        print(f"   コード: {chord_symbol}, キー: {main_key}")
        
        # コードの構成音を取得
        try:
            chord = Chord(chord_symbol)
            chord_notes = chord.components()
            print(f"   構成音: {chord_notes}")
        except:
            print(f"   構成音: 取得失敗")
            return
        
        # ダイアトニック音を取得
        diatonic_notes = get_diatonic_notes(main_key)
        print(f"   ダイアトニック音: {diatonic_notes}")
        
        # 正規化して比較
        normalized_chord_notes = [normalize_note(note) for note in chord_notes]
        normalized_diatonic_notes = [normalize_note(note) for note in diatonic_notes]
        
        print(f"   正規化コード構成音: {normalized_chord_notes}")
        print(f"   正規化ダイアトニック音: {normalized_diatonic_notes}")
        
        # 非ダイアトニック音をチェック
        non_diatonic_notes = [note for note in chord_notes 
                             if normalize_note(note) not in normalized_diatonic_notes]
        
        print(f"   非ダイアトニック音: {non_diatonic_notes}")
        
        if non_diatonic_notes:
            print(f"   → 借用和音として判定されるべき")
        else:
            print(f"   → ダイアトニック和音として判定される（問題！）")
        
        print()
    
    # テストケース
    test_cases = [
        ('C#dim', 'G Major'),
        ('C#dim(9)', 'G Major'),
        ('F#dim', 'G Major'),  # 比較用
        ('F#dim(9)', 'G Major'),  # 比較用
    ]
    
    for chord, key in test_cases:
        check_borrowed_chord(chord, key)
    
    print("3. 問題の分析:")
    print("   - C#dimは正しく借用和音判定される")
    print("   - C#dim(9)もpychordが正しく解析すれば借用和音判定されるはず")
    print("   - もしダイアトニック判定されるなら、pychordの解析結果に問題がある可能性")
    print("   - またはバックエンドのコード抽出ロジックでテンション部分が除去されている可能性")

if __name__ == "__main__":
    debug_tension_borrowed_issue()