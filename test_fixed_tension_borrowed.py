#!/usr/bin/env python3
"""
修正されたテンション付き借用和音検出のテスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_fixed_tension_borrowed():
    print("=== 修正されたテンション付き借用和音検出のテスト ===\n")
    
    # 修正されたget_chord_components関数をテスト
    try:
        from main import get_chord_components, get_diatonic_notes, normalize_note
        
        print("1. 修正されたget_chord_components関数のテスト:")
        test_chords = [
            'C#dim',        # 基本ディミニッシュ
            'C#dim(9)',     # テンション付きディミニッシュ（問題のケース）
            'Am7',          # 基本マイナー7th
            'Am7(9)',       # テンション付きマイナー7th
            'G7(b9)',       # テンション付きドミナント
            'FM7(#11)',     # テンション付きメジャー7th
        ]
        
        for chord_symbol in test_chords:
            components = get_chord_components(chord_symbol)
            print(f"   {chord_symbol:>12} → {components}")
        
        print()
        
        print("2. 借用和音検出テスト（Gメジャーキー）:")
        main_key = "G Major"
        diatonic_notes = get_diatonic_notes(main_key)
        normalized_diatonic_notes = [normalize_note(note) for note in diatonic_notes]
        
        print(f"   キー: {main_key}")
        print(f"   ダイアトニック音: {diatonic_notes}")
        print(f"   正規化ダイアトニック音: {normalized_diatonic_notes}")
        print()
        
        test_cases = [
            'C#dim',        # 借用和音であるべき
            'C#dim(9)',     # 借用和音であるべき（修正対象）
            'F#dim',        # ダイアトニック（vii°）
            'F#dim(9)',     # ダイアトニックであるべき
            'Bm7',          # ダイアトニック（iii）
            'Bm7(9)',       # ダイアトニックであるべき
        ]
        
        for chord_symbol in test_cases:
            chord_notes = get_chord_components(chord_symbol)
            print(f"   {chord_symbol:>12}:")
            print(f"     構成音: {chord_notes}")
            
            if chord_notes:
                normalized_chord_notes = [normalize_note(note) for note in chord_notes]
                non_diatonic_notes = [note for note in chord_notes 
                                    if normalize_note(note) not in normalized_diatonic_notes]
                
                print(f"     正規化構成音: {normalized_chord_notes}")
                print(f"     非ダイアトニック音: {non_diatonic_notes}")
                
                if non_diatonic_notes:
                    print(f"     判定: 借用和音 ✓")
                else:
                    print(f"     判定: ダイアトニック")
            else:
                print(f"     判定: 構成音取得失敗")
            print()
        
        print("3. 期待される結果:")
        expected_results = {
            'C#dim': '借用和音',
            'C#dim(9)': '借用和音（修正後）',
            'F#dim': 'ダイアトニック',
            'F#dim(9)': 'ダイアトニック',
            'Bm7': 'ダイアトニック',
            'Bm7(9)': 'ダイアトニック'
        }
        
        for chord, expected in expected_results.items():
            print(f"   {chord:>12} → {expected}")
            
    except ImportError as e:
        print(f"インポートエラー: {e}")
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    test_fixed_tension_borrowed()