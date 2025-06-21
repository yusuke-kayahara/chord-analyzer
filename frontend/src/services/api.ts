import axios from 'axios';
import { ChordAnalysisRequest, ChordAnalysisResponse } from '../types/chord';

// API設定
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// コード進行分析API
export const analyzeChordProgression = async (
  chordInput: string
): Promise<ChordAnalysisResponse> => {
  try {
    const request: ChordAnalysisRequest = {
      chord_input: chordInput,
    };

    const response = await api.post<ChordAnalysisResponse>('/analyze', request);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        `API Error: ${error.response?.status} - ${error.response?.data?.detail || error.message}`
      );
    }
    throw new Error('Unknown error occurred while analyzing chord progression');
  }
};

// API接続テスト
export const testApiConnection = async (): Promise<boolean> => {
  try {
    const response = await api.get('/');
    return response.status === 200;
  } catch (error) {
    console.error('API connection test failed:', error);
    return false;
  }
};

export default api;