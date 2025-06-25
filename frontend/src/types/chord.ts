// コード進行分析のTypeScript型定義
export interface ChordAnalysisRequest {
  chord_input: string;
  algorithm?: string; // "traditional", "borrowed_chord_minimal", "triad_ratio", "hybrid", "manual"
  traditional_weight?: number;
  borrowed_chord_weight?: number;
  triad_ratio_weight?: number;
  manual_key?: string; // 手動指定キー
}

export interface KeyCandidate {
  key: string;
  relationship: string;
  confidence: number;
}

export interface BorrowedChord {
  chord: string;
  non_diatonic_notes: string[];
  source_candidates: KeyCandidate[];
}

export interface KeyEstimationResult {
  key: string;
  confidence: number;
  borrowed_chord_count: number;
  algorithm: string;
}

export interface ProgressionDetail {
  chord_symbol: string;
  components: string[];
}

export interface AnalysisResponse {
  main_key: string;
  confidence: float;
  borrowed_chords: any[]; // Replace with a more specific type if you have one
  pitch_class_vector: number[];
  key_candidates: any[]; // Replace with a more specific type if you have one
  algorithm_used: string;
  progression_details: ProgressionDetail[];
}

export interface UIState {
  isAnalyzing: boolean;
  error: string | null;
  result: AnalysisResponse | null;
}

export interface AdvancedSettings {
  algorithm: string;
  traditional_weight: number;
  borrowed_chord_weight: number;
  triad_ratio_weight: number;
  manual_key: string;
  showAdvanced: boolean;
}

export interface SelectedBorrowedKeys {
  [chordName: string]: string; // コード名 -> 選択された借用元キー
}

export interface AnalysisHistory {
  id: string;
  timestamp: number;
  chord_input: string;
  settings: {
    algorithm: string;
    traditional_weight: number;
    borrowed_chord_weight: number;
    triad_ratio_weight: number;
    manual_key: string;
  };
  result: AnalysisResponse;
}