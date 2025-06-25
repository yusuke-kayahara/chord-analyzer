#!/usr/bin/env python3
"""
C(#9)の借用和音判定問題をデバッグ
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def debug_c_sharp9_issue():
    print("=== C(#9) 借用和音判定問題のデバッグ ===\n")
    
    try:
        from main import (
            get_chord_components, get_diatonic_notes, normalize_note,
            detect_non_diatonic_notes, extract_chords
        )
        
        print("1. C(#9)の構成音分析:")
        chord_symbol = "C(#9)"
        components = get_chord_components(chord_symbol)
        print(f"   コード: {chord_symbol}")
        print(f"   構成音: {components}")
        
        # pychordでの直接分析もテスト
        try:
            from pychord import Chord
            print(f"\n   pychord直接解析:")
            chord_obj = Chord(chord_symbol)
            print(f"   構成音: {chord_obj.components()}")
        except Exception as e:
            print(f"   pychordエラー: {e}")
            
            # コア部分での解析
            try:
                core_chord = Chord("C")
                print(f"   コア部分(C)の構成音: {core_chord.components()}")
            except Exception as e2:
                print(f"   コア部分もエラー: {e2}")
        
        print(f"\n2. Cメジャーキーのダイアトニック音:")
        main_key = "C Major"
        diatonic_notes = get_diatonic_notes(main_key)
        print(f"   ダイアトニック音: {diatonic_notes}")
        
        print(f"\n3. 期待される#9音の分析:")
        print(f"   C(#9)に含まれるべき音:")
        print(f"   - C (ルート)")
        print(f"   - E (3度)")
        print(f"   - G (5度)")
        print(f"   - D# (#9度) ← これが非ダイアトニック！")
        print(f"   ")
        print(f"   Cメジャーキーでは D (レ) がダイアトニックだが、")
        print(f"   C(#9) では D# (レ#) が使われるため借用和音であるべき")
        
        print(f"\n4. 実際の借用和音検出テスト:")
        test_input = "[C(#9)]"
        chords = extract_chords(test_input)
        print(f"   入力: {test_input}")
        print(f"   抽出コード: {chords}")
        
        non_diatonic_chords = detect_non_diatonic_notes(chords, main_key)
        print(f"   非ダイアトニック判定: {[chord['chord'] for chord in non_diatonic_chords]}")
        
        if non_diatonic_chords:
            print(f"   → 正しく借用和音として判定された ✓")
            for chord in non_diatonic_chords:
                print(f"     非ダイアトニック音: {chord['non_diatonic_notes']}")
        else:
            print(f"   → 問題！ダイアトニックとして判定されている ✗")
            
        print(f"\n5. 他のテンションコードのテスト:")
        test_chords = ["C(b9)", "C(#11)", "C(b13)", "C(#9,#11)", "G7(#9)"]
        for test_chord in test_chords:
            components = get_chord_components(test_chord)
            test_input = f"[{test_chord}]"
            chords = extract_chords(test_input)
            non_diatonic = detect_non_diatonic_notes(chords, main_key)
            
            status = "借用和音" if non_diatonic else "ダイアトニック"
            print(f"   {test_chord:>10} (構成音: {components}) → {status}")
            
        print(f"\n6. 問題の原因分析:")
        print(f"   - pychordがテンション付きコードを正しく解析できない場合")
        print(f"   - get_chord_components()でコア部分のみ抽出している")
        print(f"   - テンション音(#9, b9等)が構成音に含まれない")
        print(f"   - そのためテンション由来の非ダイアトニック音が検出されない")
        
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_c_sharp9_issue()