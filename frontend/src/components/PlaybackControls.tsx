import React, { useState, useEffect, useRef, useCallback } from 'react';
import * as Tone from 'tone';
import { ProgressionDetail } from '../types/chord';
import PianoKeyboard from './PianoKeyboard';

interface PlaybackControlsProps {
  progression: ProgressionDetail[];
}

const PlaybackControls: React.FC<PlaybackControlsProps> = ({ progression }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentChordIndex, setCurrentChordIndex] = useState(-1);
  // Set default volume to -20dB (around 50% perception)
  const [volume, setVolume] = useState(-20);

  const synthRef = useRef<Tone.PolySynth | null>(null);
  const volumeRef = useRef<Tone.Volume | null>(null);
  const sequenceRef = useRef<Tone.Sequence | null>(null);

  useEffect(() => {
    volumeRef.current = new Tone.Volume(volume).toDestination();
    synthRef.current = new Tone.PolySynth(Tone.Synth, {
      oscillator: { type: 'triangle' },
      envelope: { attack: 0.02, decay: 0.1, sustain: 0.3, release: 1 }
    }).connect(volumeRef.current);

    return () => {
      synthRef.current?.dispose();
      volumeRef.current?.dispose();
      Tone.Transport.stop();
      Tone.Transport.cancel();
    };
  }, []); // Empty dependency array ensures this runs only once

  useEffect(() => {
    if (volumeRef.current) {
      volumeRef.current.volume.value = volume;
    }
  }, [volume]);

  useEffect(() => {
    if (sequenceRef.current) {
      sequenceRef.current.dispose();
    }
    Tone.Transport.stop();
    setIsPlaying(false);
    setCurrentChordIndex(-1);
    
    if (progression.length > 0 && synthRef.current) {
      const newSequence = new Tone.Sequence(
        (time, chord) => {
          // Backend now provides notes with octave, so no need to add '4'
          const notes = chord.components;
          // Use '2n' for a half note duration
          synthRef.current?.triggerAttackRelease(notes, '2n', time);
          Tone.Draw.schedule(() => {
            setCurrentChordIndex(progression.indexOf(chord));
          }, time);
        },
        progression,
        '2n' // The sequence interval is now also '2n'
      );
      newSequence.loop = false;
      sequenceRef.current = newSequence;
    }
  }, [progression]);

  const handlePlayPause = useCallback(async () => {
    if (!sequenceRef.current) return;

    if (Tone.context.state !== 'running') {
      await Tone.start();
    }

    if (isPlaying) {
      Tone.Transport.pause();
      setIsPlaying(false);
    } else {
      Tone.Transport.start();
      sequenceRef.current.start(0);
      setIsPlaying(true);
    }
  }, [isPlaying]);

  const handleStop = useCallback(() => {
    Tone.Transport.stop();
    setIsPlaying(false);
    setCurrentChordIndex(-1);
  }, []);

  // 現在再生中のコードの構成音を取得
  const getCurrentChordNotes = (): string[] => {
    if (currentChordIndex >= 0 && currentChordIndex < progression.length) {
      return progression[currentChordIndex].components;
    }
    return [];
  };

  // 現在のコード名を取得
  const getCurrentChordName = (): string => {
    if (currentChordIndex >= 0 && currentChordIndex < progression.length) {
      return progression[currentChordIndex].chord_symbol;
    }
    return '';
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">試聴・再生</h3>
      <div className="space-y-4">
        {/* Playback and Progress Bar */}
        <div className="flex items-center space-x-4">
          <button
            onClick={handlePlayPause}
            disabled={progression.length === 0}
            className="w-24 px-4 py-2 font-semibold text-white bg-blue-500 rounded-lg hover:bg-blue-600 transition-colors disabled:bg-gray-400"
          >
            {isPlaying ? '一時停止' : '再生'}
          </button>
          <button
            onClick={handleStop}
            disabled={progression.length === 0}
            className="w-24 px-4 py-2 font-semibold text-white bg-red-500 rounded-lg hover:bg-red-600 transition-colors disabled:bg-gray-400"
          >
            停止
          </button>
          <div className="flex-grow flex items-center space-x-2 bg-gray-200 p-1 rounded-full">
            {progression.map((_, index) => (
              <div key={index} className="flex-1 h-3 rounded-full transition-colors"
                   style={{ backgroundColor: index === currentChordIndex ? '#3B82F6' : '#E5E7EB' }}>
              </div>
            ))}
          </div>
        </div>

        {/* Current Chord Display */}
        {currentChordIndex >= 0 && (
          <div className="bg-blue-50 p-3 rounded-lg border border-blue-200">
            <p className="text-sm text-blue-800 font-medium">
              現在再生中: <span className="font-bold">{getCurrentChordName()}</span>
            </p>
          </div>
        )}

        {/* Piano Keyboard Visualization */}
        <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
          <h4 className="text-sm font-semibold text-gray-700 mb-3">構成音の視覚化</h4>
          <div className="overflow-x-auto">
            <PianoKeyboard 
              activeNotes={getCurrentChordNotes()}
              startOctave={2}
              endOctave={5}
              className="w-full"
            />
          </div>
        </div>

        {/* Volume Control */}
        <div className="flex items-center space-x-3 pt-2">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
          </svg>
          <input
            type="range"
            min="-40"
            max="0"
            step="1"
            value={volume}
            onChange={(e) => setVolume(Number(e.target.value))}
            className="w-32 h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer slider-track"
            style={{ '--value': `${((volume + 40) / 40) * 100}%` } as React.CSSProperties}
          />
        </div>
      </div>
    </div>
  );
};

export default PlaybackControls;