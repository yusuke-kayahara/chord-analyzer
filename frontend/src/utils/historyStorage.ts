import { AnalysisHistory, ChordAnalysisResponse, AdvancedSettings } from '../types/chord';

const STORAGE_KEY = 'chord-analyzer-history';
const MAX_HISTORY_ITEMS = 10; // 最大保存件数

export class HistoryStorage {
  static getHistory(): AnalysisHistory[] {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (!stored) return [];
      
      const parsed = JSON.parse(stored);
      // 時間順（新しい順）でソート
      return parsed.sort((a: AnalysisHistory, b: AnalysisHistory) => b.timestamp - a.timestamp);
    } catch (error) {
      console.error('Failed to load history:', error);
      return [];
    }
  }

  static saveAnalysis(
    chordInput: string,
    settings: AdvancedSettings,
    result: ChordAnalysisResponse
  ): void {
    try {
      const history = this.getHistory();
      
      // 新しい分析記録を作成
      const newAnalysis: AnalysisHistory = {
        id: Date.now().toString(), // 簡易ID
        timestamp: Date.now(),
        chord_input: chordInput,
        settings: {
          algorithm: settings.algorithm,
          traditional_weight: settings.traditional_weight,
          borrowed_chord_weight: settings.borrowed_chord_weight,
          triad_ratio_weight: settings.triad_ratio_weight,
          manual_key: settings.manual_key
        },
        result
      };

      // 同じコード進行+設定の組み合わせがある場合は削除（重複回避）
      const filteredHistory = history.filter(item => 
        !(item.chord_input === chordInput && 
          item.settings.algorithm === settings.algorithm &&
          item.settings.traditional_weight === settings.traditional_weight &&
          item.settings.borrowed_chord_weight === settings.borrowed_chord_weight &&
          item.settings.triad_ratio_weight === settings.triad_ratio_weight &&
          item.settings.manual_key === settings.manual_key)
      );

      // 新しい記録を先頭に追加
      const updatedHistory = [newAnalysis, ...filteredHistory];

      // 最大件数を超えた場合は古いものを削除
      const trimmedHistory = updatedHistory.slice(0, MAX_HISTORY_ITEMS);

      localStorage.setItem(STORAGE_KEY, JSON.stringify(trimmedHistory));
    } catch (error) {
      console.error('Failed to save history:', error);
    }
  }

  static clearHistory(): void {
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (error) {
      console.error('Failed to clear history:', error);
    }
  }

  static removeItem(id: string): void {
    try {
      const history = this.getHistory();
      const filtered = history.filter(item => item.id !== id);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered));
    } catch (error) {
      console.error('Failed to remove history item:', error);
    }
  }
}