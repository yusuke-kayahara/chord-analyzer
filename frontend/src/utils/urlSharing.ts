import { AdvancedSettings } from '../types/chord';

// URL共有用のエンコード・デコード機能
export class URLSharing {
  // 分析設定をURLパラメータにエンコード
  static encodeAnalysisToURL(chordInput: string, settings: AdvancedSettings): string {
    const params = new URLSearchParams();
    
    // Base64エンコードでコード進行を安全に保存
    params.set('chords', btoa(encodeURIComponent(chordInput)));
    params.set('algorithm', settings.algorithm);
    
    // 重みパラメータは小数点以下2桁まで
    if (settings.algorithm === 'hybrid') {
      params.set('tw', settings.traditional_weight.toFixed(2));
      params.set('bw', settings.borrowed_chord_weight.toFixed(2));
      params.set('rw', settings.triad_ratio_weight.toFixed(2));
    }
    
    // 手動キー指定がある場合
    if (settings.manual_key) {
      params.set('key', encodeURIComponent(settings.manual_key));
    }
    
    return `${window.location.origin}${window.location.pathname}?${params.toString()}`;
  }
  
  // URLパラメータから分析設定をデコード
  static decodeAnalysisFromURL(): { chordInput: string; settings: AdvancedSettings } | null {
    const params = new URLSearchParams(window.location.search);
    
    const chordsParam = params.get('chords');
    if (!chordsParam) return null;
    
    try {
      // Base64デコード
      const chordInput = decodeURIComponent(atob(chordsParam));
      
      const settings: AdvancedSettings = {
        algorithm: params.get('algorithm') || 'hybrid',
        traditional_weight: parseFloat(params.get('tw') || '0.2'),
        borrowed_chord_weight: parseFloat(params.get('bw') || '0.3'),
        triad_ratio_weight: parseFloat(params.get('rw') || '0.5'),
        manual_key: params.get('key') ? decodeURIComponent(params.get('key')!) : '',
        showAdvanced: false
      };
      
      return { chordInput, settings };
    } catch (error) {
      console.error('URL decoding failed:', error);
      return null;
    }
  }
  
  // URLをクリップボードにコピー
  static async copyToClipboard(url: string): Promise<boolean> {
    try {
      await navigator.clipboard.writeText(url);
      return true;
    } catch (error) {
      // フォールバック: 一時的なテキストエリアを使用
      try {
        const textArea = document.createElement('textarea');
        textArea.value = url;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        return true;
      } catch (fallbackError) {
        console.error('Clipboard copy failed:', fallbackError);
        return false;
      }
    }
  }
  
  // URLから不要なパラメータを削除
  static clearURLParams(): void {
    const url = new URL(window.location.href);
    url.search = '';
    window.history.replaceState({}, '', url.toString());
  }
}