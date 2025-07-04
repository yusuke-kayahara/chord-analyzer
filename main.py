from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import re
import numpy as np
from pychord import Chord
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="Chord Progression Analyzer", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 一時的に全て許可（デバッグ用）
    allow_credentials=False,  # "*"使用時はcredentialsをFalseに
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChordAnalysisRequest(BaseModel):
    chord_input: str
    algorithm: str = "hybrid"  # "traditional", "borrowed_chord_minimal", "triad_ratio", "hybrid", "manual"
    traditional_weight: float = 0.2  # Krumhansl類似度の重み
    borrowed_chord_weight: float = 0.3  # 借用和音最小化の重み
    triad_ratio_weight: float = 0.5  # トライアド比率分析の重み
    manual_key: str = None  # 手動指定キー（例: "C Major", "A Minor"）

class KeyCandidate(BaseModel):
    key: str
    relationship: str
    confidence: float

class BorrowedChord(BaseModel):
    chord: str
    non_diatonic_notes: List[str]
    source_candidates: List[KeyCandidate]

class KeyEstimationResult(BaseModel):
    key: str
    confidence: float
    borrowed_chord_count: int
    algorithm: str

class ProgressionDetail(BaseModel):
    chord_symbol: str
    components: List[str]

class AnalysisResponse(BaseModel):
    main_key: str
    confidence: float
    borrowed_chords: List[BorrowedChord]
    pitch_class_vector: List[float]
    key_candidates: List[KeyEstimationResult]  # 各アルゴリズムの結果
    algorithm_used: str
    progression_details: List[ProgressionDetail]

# Constants
NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Krumhansl's key profiles
KRUMHANSL_MAJOR = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
KRUMHANSL_MINOR = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

def is_valid_chord(chord: str) -> bool:
    """コードが有効かどうかを判定"""
    # 空文字、空白のみ、特殊文字のみは無効
    if not chord or chord.strip() == '' or chord.strip() == '|':
        return False
    
    # 基本的なコード形式をチェック（A-G で始まる）
    chord_pattern = r'^[A-G][#b]?'
    return bool(re.match(chord_pattern, chord.strip()))

def extract_chords(chord_input: str) -> List[str]:
    """[]で囲まれたコードを抽出する（無効なコードを除外）"""
    pattern = r'\[([^\]]+)\]'
    matches = re.findall(pattern, chord_input)
    # 有効なコードのみをフィルタリング
    valid_chords = [chord.strip() for chord in matches if is_valid_chord(chord.strip())]
    return valid_chords

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

def get_chord_components(chord_symbol: str) -> List[str]:
    """コード構成音を取得（括弧記法テンション対応）"""
    import re
    
    # 括弧記法の分解: Bm7(13) -> コア部分="Bm7", テンション部分="13"
    tension_match = re.match(r'^([A-G][#b]?(?:maj|m|dim|aug|sus[24]?)?(?:7|maj7|mM7|M7|6|add\d+)?)\(([^)]+)\)$', chord_symbol)
    
    if tension_match:
        core_chord_str = tension_match.group(1)
        tension_part = tension_match.group(2)
        
        try:
            # コア部分をpychordで解析
            core_chord = Chord(core_chord_str)
            core_notes = core_chord.components()
            
            # テンション音を独自ロジックで追加
            tension_notes = calculate_tension_notes_advanced(core_chord_str, tension_part)
            
            # 重複除去して結合
            all_notes = core_notes[:]
            for note in tension_notes:
                if note not in all_notes:
                    all_notes.append(note)
            
            return all_notes
            
        except Exception as e:
            print(f"Error processing bracketed chord {chord_symbol}: {e}")
            pass
    
    # 通常のコード処理
    try:
        chord = Chord(chord_symbol)
        return chord.components()
    except Exception:
        # 最後の手段：括弧を除去して再試行
        try:
            simplified = re.sub(r'\([^)]*\)', '', chord_symbol)
            chord = Chord(simplified)
            return chord.components()
        except Exception:
            return []
        # テンション付きコードの場合、コア部分とテンション部分を分けて処理
        try:
            import re
            
            # テンション部分を抽出
            tension_match = re.match(r'^([A-G][#b]?(?:maj|m|dim|aug|sus[24]?)?(?:7|maj7|mM7|M7)?)\(([^)]+)\)', chord_symbol)
            
            if tension_match:
                core_chord_str = tension_match.group(1)
                tension_part = tension_match.group(2)
                
                # コア部分の構成音を取得
                chord = Chord(core_chord_str)
                base_components = chord.components()
                
                # テンション音を計算して追加
                tension_notes = calculate_tension_notes(core_chord_str, tension_part)
                
                # 重複を除去して結合
                all_components = list(set(base_components + tension_notes))
                return all_components
            else:
                # テンション記法がない場合、コア部分のみで解析
                core_match = re.match(r'^([A-G][#b]?(?:maj|m|dim|aug|sus[24]?)?(?:7|maj7|mM7|M7)?)', chord_symbol)
                if core_match:
                    core_chord = core_match.group(1)
                    chord = Chord(core_chord)
                    return chord.components()
                else:
                    return []
        except Exception:
            return []

def calculate_tension_notes_advanced(core_chord: str, tension_part: str) -> List[str]:
    """高度なテンション計算（独自ロジック）"""
    tension_notes = []
    
    try:
        # コードのルート音を取得
        from pychord import Chord
        chord_obj = Chord(core_chord)
        root_note = str(chord_obj.root)
        root_pc = note_to_pitch_class(root_note)
        
        # テンション要素を分割・解析
        tension_elements = re.split(r'[,、\s]+', tension_part)
        
        for element in tension_elements:
            element = element.strip()
            if not element:
                continue
                
            # テンション記法を解析 (例: 9, #11, b13, 13)
            tension_match = re.match(r'([#b+-]?)(\d+)', element)
            if tension_match:
                modifier = tension_match.group(1) if tension_match.group(1) else ''
                number = int(tension_match.group(2))
                
                # テンション音のピッチクラスを計算
                tension_pc = calculate_tension_pitch_class_advanced(root_pc, number, modifier)
                if tension_pc is not None:
                    tension_note = NOTES[tension_pc]
                    tension_notes.append(tension_note)
    
    except Exception as e:
        print(f"Error calculating tension for {core_chord}({tension_part}): {e}")
    
    return tension_notes

def calculate_tension_notes(core_chord: str, tension_part: str) -> List[str]:
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
    
    except Exception:
        pass
    
    return tension_notes

def calculate_tension_pitch_class_advanced(root_pc: int, interval: int, modifier: str) -> int:
    """高度なテンション音ピッチクラス計算"""
    # より正確なインターバルマッピング
    interval_map = {
        # 基本度数
        2: 2,   # 2度 = 2半音
        4: 5,   # 4度 = 5半音
        6: 9,   # 6度 = 9半音
        7: 10,  # 7度 = 10半音（短7度）
        # テンション度数（オクターブ上の度数）
        9: 2,   # 9度 = 2度 (2半音)
        11: 5,  # 11度 = 4度 (5半音)
        13: 9,  # 13度 = 6度 (9半音)
    }
    
    base_interval = interval_map.get(interval)
    if base_interval is None:
        return None
    
    # 修飾記号を適用
    if modifier == '#' or modifier == '+':
        base_interval += 1
    elif modifier == 'b' or modifier == '-':
        base_interval -= 1
    
    # ルートからの音程を計算
    tension_pc = (root_pc + base_interval) % 12
    return tension_pc

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

def optimize_root_octave(root_pc: int, core_notes: List[tuple], base_root_octave: int, base_octave: int) -> int:
    """ルートオクターブを最適化（実際のボイシング後の音高を考慮）"""
    if not core_notes:
        # コア音がない場合は1オクターブ上げて自然なレンジにする
        return base_root_octave + 1
    
    # 各コア音の実際の配置オクターブを予測
    core_octave = base_octave
    last_pc = -1
    actual_core_notes = []
    
    for note, interval in sorted(core_notes, key=lambda x: x[1]):
        pc = note_to_pitch_class(note)
        if pc < last_pc:  # 音が下行する場合はオクターブを上げる
            core_octave += 1
        actual_core_notes.append((note, pc, core_octave))
        last_pc = pc
    
    # 最低コア音の実際のMIDI番号を計算
    lowest_core_midi = min((octave + 1) * 12 + pc for _, pc, octave in actual_core_notes)
    
    # ルートを1オクターブ上げた場合のMIDI番号
    optimized_root_midi = (base_root_octave + 1 + 1) * 12 + root_pc
    
    # ルートが最低音を維持できるかチェック
    if optimized_root_midi < lowest_core_midi:
        return base_root_octave + 1
    else:
        return base_root_octave

def get_chord_components_with_voicing(chord_symbol: str, base_octave: int = 3) -> List[str]:
    """コード構成音を、音楽理論に基づいた自然なボイシングで取得する"""
    try:
        components = get_chord_components(chord_symbol)
        if not components:
            return []

        root_note = components[0]
        root_pc = note_to_pitch_class(root_note)

        # 音程に基づいて構成音を分類（ルート、コア音、テンション音）
        root_notes = []      # ルート音
        core_notes = []      # 3rd, 5th, 7th
        tension_notes = []   # 9th, 11th, 13th
        
        # 括弧記法で追加されたテンション音を特定
        bracket_tensions = []
        if '(' in chord_symbol and ')' in chord_symbol:
            # コア部分とテンション部分を分離
            import re
            tension_match = re.match(r'^([A-G][#b]?(?:maj|m|dim|aug|sus[24]?)?(?:7|maj7|mM7|M7|6|add\d+)?)\(([^)]+)\)$', chord_symbol)
            if tension_match:
                core_chord_str = tension_match.group(1)
                try:
                    core_chord = Chord(core_chord_str)
                    core_components = core_chord.components()
                    # コア音以外はテンション音
                    bracket_tensions = [note for note in components if note not in core_components]
                except:
                    pass
        
        for note in components:
            pc = note_to_pitch_class(note)
            interval = (pc - root_pc + 12) % 12
            
            # 括弧記法で追加された音は強制的にテンション分類
            if note in bracket_tensions:
                tension_notes.append((note, interval))
            elif interval == 0:  # ルート
                root_notes.append((note, interval))
            elif interval in [1, 2]:  # 9th (2nd)
                tension_notes.append((note, interval))
            elif interval in [3, 4]:  # 3rd
                core_notes.append((note, interval))
            elif interval in [5, 6]:  # 4th/11th
                if '11' in chord_symbol or 'sus4' in chord_symbol:
                    if '11' in chord_symbol:
                        tension_notes.append((note, interval))
                    else:
                        core_notes.append((note, interval))
                else:
                    core_notes.append((note, interval))
            elif interval == 7:  # 5th
                core_notes.append((note, interval))
            elif interval in [8, 9]:  # 6th/13th
                if '13' in chord_symbol:
                    tension_notes.append((note, interval))
                else:
                    core_notes.append((note, interval))
            elif interval in [10, 11]:  # 7th
                core_notes.append((note, interval))
            else:
                core_notes.append((note, interval))
        
        # 各グループ内で音程順にソート
        core_notes.sort(key=lambda x: x[1])
        tension_notes.sort(key=lambda x: x[1])
        
        # 新しいボイシングロジック：コア音中心配置
        voiced_notes = []
        
        # 1. コア音を中心オクターブ（base_octave）に配置
        core_octave = base_octave
        last_core_pc = -1
        
        for note, interval in core_notes:
            pc = note_to_pitch_class(note)
            if pc < last_core_pc:  # 音が下行する場合はオクターブを上げる
                core_octave += 1
            voiced_notes.append(f"{note}{core_octave}")
            last_core_pc = pc
        
        # 2. ルート音を最適なオクターブに配置
        if root_notes:
            root_note, _ = root_notes[0]
            root_pc = note_to_pitch_class(root_note)
            
            # 基本ルートオクターブ
            base_root_octave = base_octave - 1 if base_octave > 1 else base_octave
            
            # ルートオクターブ最適化: ルートを上げても音列が崩れないかチェック
            optimized_root_octave = optimize_root_octave(root_pc, core_notes, base_root_octave, base_octave)
            
            # ルート音をリストの最初に挿入
            voiced_notes.insert(0, f"{root_note}{optimized_root_octave}")
        
        # 3. テンション音をコア音より高く配置
        for note, interval in tension_notes:
            # テンション音は常にコア音より高いオクターブに配置
            tension_octave = core_octave + 1
            voiced_notes.append(f"{note}{tension_octave}")

        print(f"Voicing for {chord_symbol}: {voiced_notes}") # DEBUGGING PRINT
        return voiced_notes

    except Exception as e:
        print(f"Error in voicing {chord_symbol}: {e}")
        return [f"{n}{base_octave}" for n in get_chord_components(chord_symbol)]

def create_pitch_class_vector(chords: List[str]) -> np.ndarray:
    """12次元ピッチクラスベクトルを作成（改良版：重み付けあり）"""
    vector = np.zeros(12)
    
    for chord_index, chord_symbol in enumerate(chords):
        notes = get_chord_components(chord_symbol)
        
        # 1つ目のコードに追加重み（最初のコードは重要）
        chord_weight = 2.0 if chord_index == 0 else 1.0
        
        for note_index, note in enumerate(notes):
            pitch_class = note_to_pitch_class(note)
            
            # ルート音（最初の音）により大きな重み
            note_weight = 2.0 if note_index == 0 else 1.0
            
            vector[pitch_class] += chord_weight * note_weight
    
    # 正規化
    if np.sum(vector) > 0:
        vector = vector / np.sum(vector)
    
    return vector

def rotate_profile(profile: List[float], root: int) -> List[float]:
    """キープロファイルを指定したルートに回転"""
    return profile[root:] + profile[:root]

def find_best_key(pitch_vector: np.ndarray):
    """最適なキーを見つける（改良版：重要音重み付けあり）"""
    best_similarity = -1
    best_key = None
    
    for root in range(12):
        # メジャーキーとの類似度（重み付きベクトルで比較）
        enhanced_vector = pitch_vector.copy()
        
        # メジャーキーの重要音に重み付け
        tonic = root % 12
        third = (root + 4) % 12
        fifth = (root + 7) % 12
        
        if enhanced_vector[tonic] > 0:
            enhanced_vector[tonic] *= 1.5
        if enhanced_vector[third] > 0:
            enhanced_vector[third] *= 1.3
        if enhanced_vector[fifth] > 0:
            enhanced_vector[fifth] *= 1.4
        
        major_profile = rotate_profile(KRUMHANSL_MAJOR, root)
        similarity = cosine_similarity([enhanced_vector], [major_profile])[0][0]
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_key = f"{NOTES[root]} Major"
            
        # マイナーキーとの類似度（重み付きベクトルで比較）
        enhanced_vector = pitch_vector.copy()
        
        # マイナーキーの重要音に重み付け
        tonic = root % 12
        third = (root + 3) % 12  # 短3度
        fifth = (root + 7) % 12
        
        if enhanced_vector[tonic] > 0:
            enhanced_vector[tonic] *= 1.5
        if enhanced_vector[third] > 0:
            enhanced_vector[third] *= 1.3
        if enhanced_vector[fifth] > 0:
            enhanced_vector[fifth] *= 1.4
        
        minor_profile = rotate_profile(KRUMHANSL_MINOR, root)
        similarity = cosine_similarity([enhanced_vector], [minor_profile])[0][0]
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_key = f"{NOTES[root]} Minor"
    
    return best_key, best_similarity

def find_key_by_borrowed_chord_minimization(chords: List[str]):
    """借用和音が最少になるキーを探す"""
    all_keys = get_all_keys()
    best_key = None
    min_borrowed_count = float('inf')
    best_confidence = 0
    
    for key in all_keys:
        diatonic_notes = get_diatonic_notes(key)
        normalized_diatonic_notes = [normalize_note(note) for note in diatonic_notes]
        
        borrowed_count = 0
        total_chord_notes = 0
        matching_notes = 0
        
        for chord_symbol in chords:
            chord_notes = get_chord_components(chord_symbol)
            total_chord_notes += len(chord_notes)
            
            # このコードが借用和音かどうかをチェック
            normalized_chord_notes = [normalize_note(note) for note in chord_notes]
            non_diatonic_notes = [note for note in chord_notes 
                                if normalize_note(note) not in normalized_diatonic_notes]
            
            if non_diatonic_notes:
                borrowed_count += 1
            
            # マッチする音の数もカウント（信頼度計算用）
            for note in chord_notes:
                if normalize_note(note) in normalized_diatonic_notes:
                    matching_notes += 1
        
        # 信頼度 = ダイアトニック音の割合
        confidence = matching_notes / total_chord_notes if total_chord_notes > 0 else 0
        
        # より少ない借用和音、同じ借用和音数なら高い信頼度を優先
        if (borrowed_count < min_borrowed_count or 
            (borrowed_count == min_borrowed_count and confidence > best_confidence)):
            min_borrowed_count = borrowed_count
            best_key = key
            best_confidence = confidence
    
    return best_key, best_confidence, min_borrowed_count

def find_key_by_triad_ratio_analysis(pitch_vector: np.ndarray):
    """構成音分布でトライアド（1,3,5度）比率が高いキーを優先する"""
    best_key = None
    best_score = -1
    best_confidence = 0
    
    all_keys = get_all_keys()
    
    for key in all_keys:
        parts = key.split()
        if len(parts) != 2:
            continue
            
        root_note = parts[0]
        key_type = parts[1]
        
        try:
            root_pc = note_to_pitch_class(root_note)
        except:
            continue
        
        # キーのトライアド音程を計算
        if key_type == "Major":
            third_pc = (root_pc + 4) % 12  # 長3度
            fifth_pc = (root_pc + 7) % 12  # 完全5度
        else:  # Minor
            third_pc = (root_pc + 3) % 12  # 短3度
            fifth_pc = (root_pc + 7) % 12  # 完全5度
        
        # トライアド音の構成音分布での比率を計算
        triad_ratio = pitch_vector[root_pc] + pitch_vector[third_pc] + pitch_vector[fifth_pc]
        total_distribution = np.sum(pitch_vector)
        
        if total_distribution > 0:
            triad_percentage = triad_ratio / total_distribution
        else:
            triad_percentage = 0
        
        # スコア計算：トライアド比率に重み付け
        # トライアド比率が高いほど、そのキーである可能性が高い
        base_confidence = min(triad_percentage * 2.0, 1.0)  # 最大100%
        
        # 追加ボーナス：トライアドが完全に揃っている場合
        triad_completeness = 0
        if pitch_vector[root_pc] > 0:
            triad_completeness += 0.4  # ルート音
        if pitch_vector[third_pc] > 0:
            triad_completeness += 0.3  # 3度
        if pitch_vector[fifth_pc] > 0:
            triad_completeness += 0.3  # 5度
        
        # 最終スコア = トライアド比率 + 完全性ボーナス
        final_score = triad_percentage + (triad_completeness * 0.3)
        
        if final_score > best_score:
            best_score = final_score
            best_key = key
            best_confidence = base_confidence
    
    return best_key, best_confidence, best_score

# ダイアトニックスケール定義
MAJOR_SCALE_INTERVALS = [0, 2, 4, 5, 7, 9, 11]  # W-W-H-W-W-W-H
MINOR_SCALE_INTERVALS = [0, 2, 3, 5, 7, 8, 10]  # W-H-W-W-H-W-W
HARMONIC_MINOR_INTERVALS = [0, 2, 3, 5, 7, 8, 11]  # W-H-W-W-H-W+H-H (7度が短7度→長7度)

def get_diatonic_notes(key: str) -> List[str]:
    """指定されたキーのダイアトニック音を取得"""
    parts = key.split()
    if len(parts) < 2:
        return []
    
    root_note = parts[0]
    key_type = " ".join(parts[1:])  # "Harmonic Minor"のように複数語に対応
    
    try:
        root_pc = note_to_pitch_class(root_note)
    except:
        return []
    
    if key_type == "Major":
        intervals = MAJOR_SCALE_INTERVALS
    elif key_type == "Minor":
        intervals = MINOR_SCALE_INTERVALS
    elif key_type == "Harmonic Minor":
        intervals = HARMONIC_MINOR_INTERVALS
    else:
        return []
    
    diatonic_notes = []
    for interval in intervals:
        pc = (root_pc + interval) % 12
        diatonic_notes.append(NOTES[pc])
    
    return diatonic_notes

def detect_non_diatonic_notes(chords: List[str], main_key: str) -> List[dict]:
    """非ダイアトニック音を含むコードを検出"""
    diatonic_notes = get_diatonic_notes(main_key)
    non_diatonic_chords = []
    
    for chord_symbol in chords:
        chord_notes = get_chord_components(chord_symbol)
        # 正規化して比較
        normalized_chord_notes = [normalize_note(note) for note in chord_notes]
        normalized_diatonic_notes = [normalize_note(note) for note in diatonic_notes]
        non_diatonic_notes = [note for note in chord_notes 
                             if normalize_note(note) not in normalized_diatonic_notes]
        
        if non_diatonic_notes:
            non_diatonic_chords.append({
                'chord': chord_symbol,
                'non_diatonic_notes': non_diatonic_notes
            })
    
    return non_diatonic_chords

def get_all_keys() -> List[str]:
    """全24キー（メジャー・マイナー）のリストを取得（主要キー推定用）"""
    keys = []
    for note in NOTES:
        keys.append(f"{note} Major")
        keys.append(f"{note} Minor")
    return keys

def get_all_keys_for_borrowing() -> List[str]:
    """借用元候補のキーリストを取得（ハーモニックマイナー含む）"""
    keys = []
    for note in NOTES:
        keys.append(f"{note} Major")
        keys.append(f"{note} Minor")
        keys.append(f"{note} Harmonic Minor")  # 借用元候補として追加
    return keys

def find_borrowed_sources(non_diatonic_chords: List[dict], main_key: str, all_chords: List[str] = None) -> List[BorrowedChord]:
    """借用元キー候補を特定（前後のコードコンテキスト考慮）"""
    borrowing_candidates = []
    all_keys = get_all_keys_for_borrowing()  # ハーモニックマイナー含む
    
    # コード進行インデックスマップを作成（コンテキスト取得用）
    chord_index_map = {}
    if all_chords:
        for i, chord in enumerate(all_chords):
            chord_index_map[chord] = i
    
    for chord_info in non_diatonic_chords:
        chord_symbol = chord_info['chord']
        chord_notes = get_chord_components(chord_symbol)
        
        # 前後のコードの構成音を取得（コンテキスト）
        context_notes = []
        if all_chords and chord_symbol in chord_index_map:
            current_index = chord_index_map[chord_symbol]
            
            # 前のコードの構成音
            if current_index > 0:
                prev_chord = all_chords[current_index - 1]
                prev_notes = get_chord_components(prev_chord)
                context_notes.extend(prev_notes)
            
            # 次のコードの構成音
            if current_index < len(all_chords) - 1:
                next_chord = all_chords[current_index + 1]
                next_notes = get_chord_components(next_chord)
                context_notes.extend(next_notes)
        
        # 重複除去
        context_notes = list(set(context_notes)) if context_notes else None
        
        source_candidates = []
        
        # 全24キーとの照合
        for key in all_keys:
            if key == main_key:
                continue
                
            key_notes = get_diatonic_notes(key)
            # このキーですべての構成音がダイアトニックかチェック（正規化して比較）
            normalized_chord_notes = [normalize_note(note) for note in chord_notes]
            normalized_key_notes = [normalize_note(note) for note in key_notes]
            if all(note in normalized_key_notes for note in normalized_chord_notes):
                relationship = analyze_relationship(main_key, key)
                confidence = calculate_key_confidence(chord_notes, key, context_notes, main_key=main_key)
                
                source_candidates.append(KeyCandidate(
                    key=key,
                    relationship=relationship,
                    confidence=confidence
                ))
        
        # 信頼度順にソート
        source_candidates.sort(key=lambda x: x.confidence, reverse=True)
        
        borrowing_candidates.append(BorrowedChord(
            chord=chord_symbol,
            non_diatonic_notes=chord_info['non_diatonic_notes'],
            source_candidates=source_candidates[:5]  # 上位5候補（ハーモニックマイナー含むため拡張）
        ))
    
    return borrowing_candidates

def analyze_relationship(main_key: str, source_key: str) -> str:
    """メインキーと借用元キーの音楽理論的関係を分析"""
    main_parts = main_key.split()
    source_parts = source_key.split()
    
    if len(main_parts) < 2 or len(source_parts) < 2:
        return "Unknown"
    
    main_root = main_parts[0]
    main_type = " ".join(main_parts[1:])
    source_root = source_parts[0]
    source_type = " ".join(source_parts[1:])
    
    main_pc = note_to_pitch_class(main_root)
    source_pc = note_to_pitch_class(source_root)
    
    # 同じルートの場合
    if main_pc == source_pc:
        if main_type != source_type:
            if source_type == "Harmonic Minor":
                return "Parallel Harmonic Minor"
            else:
                return "Parallel Minor/Major"
        else:
            return "Same Key"
    
    # 度数関係を計算
    interval = (source_pc - main_pc) % 12
    
    interval_names = {
        0: "Unison", 1: "Minor 2nd", 2: "Major 2nd", 3: "Minor 3rd",
        4: "Major 3rd", 5: "Perfect 4th", 6: "Tritone", 7: "Perfect 5th",
        8: "Minor 6th", 9: "Major 6th", 10: "Minor 7th", 11: "Major 7th"
    }
    
    relationship = interval_names.get(interval, "Unknown")
    
    # 特別な関係性
    if interval == 9 and source_type == "Minor":  # 長6度上のマイナー（= 短3度下） 
        return "Relative Minor"
    elif interval == 3 and source_type == "Major":  # 短3度上のメジャー（= 長6度下）
        return "Relative Major"
    elif interval == 7:  # 完全5度
        return "Dominant Relationship"
    elif interval == 5:  # 完全4度
        return "Subdominant Relationship"
    elif source_type == "Harmonic Minor":
        return f"{relationship} (Harmonic Minor)"
    
    return f"{relationship} ({source_type})"

def get_key_relationship_bonus(relationship: str) -> float:
    """キー関係性に基づくconfidenceボーナスを計算"""
    # 音楽理論的に重要な関係性にボーナスを付与
    relationship_bonuses = {
        # 最重要関係（同主調・関係調）
        "Parallel Minor/Major": 0.15,          # 同主調（最も重要）
        "Parallel Harmonic Minor": 0.12,       # パラレルハーモニックマイナー
        "Relative Minor": 0.10,                # 関係調
        "Relative Major": 0.10,                # 関係調
        
        # 重要関係（機能的関係）
        "Dominant Relationship": 0.08,          # 属調（5度関係）
        "Subdominant Relationship": 0.08,      # 下属調（4度関係）
        
        # 中程度関係（近親調）
        "Major 2nd": 0.05,                     # 全音関係
        "Minor 2nd": 0.03,                     # 半音関係
        "Minor 3rd": 0.04,                     # 短3度関係
        "Major 3rd": 0.04,                     # 長3度関係
        
        # ハーモニックマイナー関係
        "Major 6th (Harmonic Minor)": 0.09,    # ハーモニックマイナー由来
        "Minor 7th (Harmonic Minor)": 0.07,    # ハーモニックマイナー由来
    }
    
    # 関係性文字列からボーナスを検索
    for key_relationship, bonus in relationship_bonuses.items():
        if key_relationship in relationship:
            return bonus
    
    # デフォルト（関係性ボーナスなし）
    return 0.0

def calculate_key_confidence(chord_notes: List[str], key: str, context_notes: List[str] = None, context_weight: float = 0.07, main_key: str = None) -> float:
    """指定されたキーに対するコードの適合度を計算（前後の和音コンテキスト・キー関係性考慮）"""
    key_notes = get_diatonic_notes(key)
    if not key_notes:
        return 0.0
    
    # メインコードの構成音に含まれる音の割合
    matching_notes = sum(1 for note in chord_notes if note in key_notes)
    if len(chord_notes) == 0:
        return 0.0
    
    basic_confidence = matching_notes / len(chord_notes)
    
    # 重要な音（ルート、3度、5度）の重み付け
    if len(chord_notes) > 0:
        root_note = chord_notes[0]  # 通常最初の音がルート
        if root_note in key_notes:
            basic_confidence += 0.1  # ルートがキーに含まれる場合はボーナス
    
    # コンテキスト（前後の和音）の構成音を考慮
    context_bonus = 0.0
    if context_notes:
        context_matching = sum(1 for note in context_notes if note in key_notes)
        if len(context_notes) > 0:
            context_confidence = context_matching / len(context_notes)
            context_bonus = context_confidence * context_weight
    
    # キー関係性ボーナスを追加
    relationship_bonus = 0.0
    if main_key and main_key != key:
        relationship = analyze_relationship(main_key, key)
        relationship_bonus = get_key_relationship_bonus(relationship)
    
    total_confidence = basic_confidence + context_bonus + relationship_bonus
    return min(total_confidence, 1.0)

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_chord_progression(request: ChordAnalysisRequest):
    """コード進行を分析する（複数アルゴリズム対応）"""
    
    # ① コード抽出
    chords = extract_chords(request.chord_input)
    
    if not chords:
        return AnalysisResponse(
            main_key="Unknown",
            confidence=0.0,
            borrowed_chords=[],
            pitch_class_vector=[0.0] * 12,
            key_candidates=[],
            algorithm_used=request.algorithm
        )
    
    # ② 構成音抽出・ベクトル化
    pitch_vector = create_pitch_class_vector(chords)
    
    # ③ 各アルゴリズムでキー推定
    key_candidates = []
    
    # 従来のアルゴリズム（Krumhansl）
    traditional_key, traditional_confidence = find_best_key(pitch_vector)
    traditional_borrowed_count = len(detect_non_diatonic_notes(chords, traditional_key))
    key_candidates.append(KeyEstimationResult(
        key=traditional_key,
        confidence=traditional_confidence,
        borrowed_chord_count=traditional_borrowed_count,
        algorithm="traditional"
    ))
    
    # 借用和音最小化アルゴリズム
    minimal_key, minimal_confidence, minimal_borrowed_count = find_key_by_borrowed_chord_minimization(chords)
    key_candidates.append(KeyEstimationResult(
        key=minimal_key,
        confidence=minimal_confidence,
        borrowed_chord_count=minimal_borrowed_count,
        algorithm="borrowed_chord_minimal"
    ))
    
    # トライアド比率分析アルゴリズム
    triad_key, triad_confidence, triad_score = find_key_by_triad_ratio_analysis(pitch_vector)
    triad_borrowed_count = len(detect_non_diatonic_notes(chords, triad_key))
    key_candidates.append(KeyEstimationResult(
        key=triad_key,
        confidence=triad_confidence,
        borrowed_chord_count=triad_borrowed_count,
        algorithm="triad_ratio"
    ))
    
    # ④ アルゴリズム選択
    if request.algorithm == "manual" and request.manual_key:
        # 手動キー指定モード
        main_key = request.manual_key
        final_confidence = 1.0  # 手動指定なので信頼度は100%
        
        # 手動指定キーの結果を候補に追加
        manual_borrowed_count = len(detect_non_diatonic_notes(chords, main_key))
        key_candidates.append(KeyEstimationResult(
            key=main_key,
            confidence=1.0,
            borrowed_chord_count=manual_borrowed_count,
            algorithm="manual"
        ))
        
    elif request.algorithm == "traditional":
        main_key = traditional_key
        final_confidence = traditional_confidence
    elif request.algorithm == "borrowed_chord_minimal":
        main_key = minimal_key
        final_confidence = minimal_confidence
    elif request.algorithm == "triad_ratio":
        main_key = triad_key
        final_confidence = triad_confidence
    else:  # hybrid
        # 3つのアルゴリズムの重み付きスコア計算
        traditional_score = traditional_confidence * request.traditional_weight
        minimal_score = (1.0 - minimal_borrowed_count / len(chords)) * request.borrowed_chord_weight
        triad_score = triad_score * request.triad_ratio_weight
        
        # 最高スコアのアルゴリズムを選択
        scores = [
            (traditional_score, traditional_key, traditional_confidence),
            (minimal_score, minimal_key, minimal_confidence),
            (triad_score, triad_key, triad_confidence)
        ]
        
        best_score, best_key_result, best_confidence_result = max(scores, key=lambda x: x[0])
        main_key = best_key_result
        final_confidence = best_confidence_result
    
    # ⑤ 借用和音検出
    non_diatonic_chords = detect_non_diatonic_notes(chords, main_key)
    borrowed_chords = find_borrowed_sources(non_diatonic_chords, main_key, chords)

    # ⑥ コード詳細の生成
    progression_details = [
        ProgressionDetail(chord_symbol=c, components=get_chord_components_with_voicing(c))
        for c in chords
    ]
    
    return AnalysisResponse(
        main_key=main_key,
        confidence=final_confidence,
        borrowed_chords=borrowed_chords,
        pitch_class_vector=pitch_vector.tolist(),
        key_candidates=key_candidates,
        algorithm_used=request.algorithm,
        progression_details=progression_details
    )

@app.get("/keys")
async def get_available_keys():
    """利用可能なキーのリストを取得"""
    return {
        "keys": get_all_keys(),
        "major_keys": [f"{note} Major" for note in NOTES],
        "minor_keys": [f"{note} Minor" for note in NOTES]
    }

@app.get("/")
async def root():
    return {"message": "Chord Progression Analyzer API"}

class VoicingDebugRequest(BaseModel):
    chord_input: str

@app.post("/debug-voicing")
async def debug_voicing(request: VoicingDebugRequest):
    """指定されたコード進行のボイシングをデバッグする"""
    chords = extract_chords(request.chord_input)
    voicings = {c: get_chord_components_with_voicing(c) for c in chords}
    return voicings

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
