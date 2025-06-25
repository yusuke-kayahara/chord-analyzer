#!/usr/bin/env python3
"""
キー関係性ボーナスのテスト
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_key_relationship_bonus():
    print("=== キー関係性ボーナステスト ===\n")
    
    try:
        from main import (
            get_key_relationship_bonus, analyze_relationship, 
            calculate_key_confidence, get_chord_components
        )
        
        print("1. get_key_relationship_bonus関数のテスト:")
        test_relationships = [
            "Parallel Minor/Major",
            "Parallel Harmonic Minor", 
            "Relative Minor",
            "Relative Major",
            "Dominant Relationship",
            "Subdominant Relationship",
            "Major 2nd",
            "Minor 3rd",
            "Perfect 5th (Major)",  # ボーナス対象外
            "Unknown relationship"   # ボーナス対象外
        ]
        
        for relationship in test_relationships:
            bonus = get_key_relationship_bonus(relationship)
            print(f"   {relationship:>30} → {bonus:+.3f}")
        
        print("\n2. analyze_relationship関数のテスト:")
        test_pairs = [
            ("C Major", "C Minor"),           # Parallel Minor/Major
            ("C Major", "C Harmonic Minor"),  # Parallel Harmonic Minor
            ("C Major", "A Minor"),           # Relative Minor
            ("A Minor", "C Major"),           # Relative Major
            ("C Major", "G Major"),           # Dominant Relationship
            ("C Major", "F Major"),           # Subdominant Relationship
            ("C Major", "D Major"),           # Major 2nd
            ("C Major", "Eb Major"),          # Minor 3rd
        ]
        
        for main_key, source_key in test_pairs:
            relationship = analyze_relationship(main_key, source_key)
            bonus = get_key_relationship_bonus(relationship)
            print(f"   {main_key:>8} → {source_key:>15} : {relationship:>30} (+{bonus:.2f})")
        
        print("\n3. calculate_key_confidence関数のテスト（関係性ボーナス含む）:")
        
        # Fmコード（F-Ab-C）をテスト
        fm_notes = get_chord_components("Fm")
        print(f"   テストコード: Fm")
        print(f"   構成音: {fm_notes}")
        print()
        
        candidate_keys = [
            ("C Minor", "Parallel Minor/Major"),     # 最高ボーナス期待
            ("C Harmonic Minor", "Parallel Harmonic Minor"),
            ("Ab Major", "Relative Major"),           # 中程度ボーナス期待
            ("F Major", "Subdominant Relationship"), # 中程度ボーナス期待
            ("Bb Major", "Major 2nd"),                # 低ボーナス期待
            ("Db Major", "Minor 2nd"),                # 低ボーナス期待
        ]
        
        main_key = "C Major"
        print(f"   メインキー: {main_key}")
        print(f"   候補キー別信頼度（関係性ボーナス適用後）:")
        
        results = []
        for candidate_key, expected_relationship in candidate_keys:
            # ボーナスなしの信頼度
            confidence_without_bonus = calculate_key_confidence(fm_notes, candidate_key)
            
            # ボーナスありの信頼度
            confidence_with_bonus = calculate_key_confidence(fm_notes, candidate_key, main_key=main_key)
            
            # 関係性とボーナス
            relationship = analyze_relationship(main_key, candidate_key)
            bonus = get_key_relationship_bonus(relationship)
            
            results.append((candidate_key, confidence_without_bonus, confidence_with_bonus, bonus, relationship))
            
            print(f"     {candidate_key:>15} : {confidence_without_bonus:.3f} → {confidence_with_bonus:.3f} (+{bonus:.3f}) [{relationship}]")
        
        print()
        print("4. 期待される効果:")
        print("   - Parallel Minor/Major (C Minor): 最高ボーナス (+0.15)")
        print("   - Parallel Harmonic Minor: 高ボーナス (+0.12)")
        print("   - Relative Major (Ab Major): 中ボーナス (+0.10)")
        print("   - Subdominant/Dominant: 中ボーナス (+0.08)")
        print("   - その他の度数関係: 低〜無ボーナス")
        
        print()
        print("5. ソート順の改善効果:")
        # ボーナス適用後のソート
        results.sort(key=lambda x: x[2], reverse=True)  # confidence_with_bonus でソート
        print("   関係性ボーナス適用後の候補順位:")
        for i, (key, conf_before, conf_after, bonus, relationship) in enumerate(results, 1):
            print(f"     {i}. {key:>15} ({conf_after:.3f}) - {relationship}")
            
    except ImportError as e:
        print(f"インポートエラー: {e}")
    except Exception as e:
        print(f"エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_key_relationship_bonus()