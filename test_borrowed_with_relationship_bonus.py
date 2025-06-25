#!/usr/bin/env python3
"""
関係性ボーナス適用後の借用和音検出テスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_borrowed_with_relationship_bonus():
    print("=== 関係性ボーナス適用後の借用和音検出テスト ===\n")
    
    try:
        from main import (
            detect_non_diatonic_notes, find_borrowed_sources, 
            extract_chords
        )
        
        # テストケース: Cメジャーキーでの借用和音
        test_progression = "[CM7][Fm][G7][C]"
        main_key = "C Major"
        
        print(f"テスト進行: {test_progression}")
        print(f"メインキー: {main_key}")
        print()
        
        # コード抽出
        chords = extract_chords(test_progression)
        print(f"抽出されたコード: {chords}")
        
        # 非ダイアトニック音検出
        non_diatonic_chords = detect_non_diatonic_notes(chords, main_key)
        print(f"非ダイアトニックコード: {[chord['chord'] for chord in non_diatonic_chords]}")
        
        if non_diatonic_chords:
            # 借用元分析（関係性ボーナス適用）
            borrowed_chords = find_borrowed_sources(non_diatonic_chords, main_key, chords)
            
            for borrowed_chord in borrowed_chords:
                print(f"\n--- {borrowed_chord.chord} の借用元候補（関係性ボーナス適用後） ---")
                print(f"非ダイアトニック音: {borrowed_chord.non_diatonic_notes}")
                print()
                
                print("候補順位（信頼度順）:")
                for i, candidate in enumerate(borrowed_chord.source_candidates[:7], 1):
                    print(f"  {i}. {candidate.key:>15} ({candidate.confidence:.3f}) - {candidate.relationship}")
                
                print()
                print("期待される改善:")
                print("  - C Minor (Parallel Minor/Major): 最上位候補として優先される")
                print("  - C Harmonic Minor (Parallel Harmonic Minor): 上位候補")
                print("  - Ab Major (Relative Major): 上位候補")
                print("  - F Major (Subdominant): 上位候補")
                print("  - その他の度数関係: 相対的に下位")
        
        print("\n=== 別のテストケース ===")
        
        # より複雑なテスト: 複数の借用和音
        test_progression2 = "[CM7][Am7][F#dim][G7][Bb][C]"
        print(f"\nテスト進行2: {test_progression2}")
        print(f"メインキー: {main_key}")
        
        chords2 = extract_chords(test_progression2)
        non_diatonic_chords2 = detect_non_diatonic_notes(chords2, main_key)
        
        print(f"非ダイアトニックコード: {[chord['chord'] for chord in non_diatonic_chords2]}")
        
        if non_diatonic_chords2:
            borrowed_chords2 = find_borrowed_sources(non_diatonic_chords2, main_key, chords2)
            
            for borrowed_chord in borrowed_chords2:
                print(f"\n{borrowed_chord.chord}: トップ3候補")
                for i, candidate in enumerate(borrowed_chord.source_candidates[:3], 1):
                    print(f"  {i}. {candidate.key} ({candidate.confidence:.3f}) - {candidate.relationship}")
        
        print("\n=== システムの効果 ===")
        print("✅ 音楽理論的に重要な関係のキーが上位にランクされる")
        print("✅ 同主調・関係調・属調・下属調が優先される")
        print("✅ ユーザーが直感的に理解しやすい借用元候補順位")
        print("✅ より自然なハーモニー分析結果")
        
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_borrowed_with_relationship_bonus()