import React, { useState, useEffect, useRef } from 'react';
import * as Tone from 'tone';
import { ProgressionDetail } from '../types/chord';

interface PlaybackControlsProps {
  progression: ProgressionDetail[];
}

const PlaybackControls: React.FC<PlaybackControlsProps> = ({ progression }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentChordIndex, setCurrentChordIndex] = useState(-1);
  const synth = useRef<Tone.PolySynth | null>(null);
  const sequence = useRef<Tone.Sequence | null>(null);

  useEffect(() => {
    // Tone.jsのシンセサイザーを初期化
    if (!synth.current) {
      synth.current = new Tone.PolySynth(Tone.Synth, {
        oscillator: {
          type: 'fmsine',
          modulationType: 'sine',
          modulationIndex: 3,
          harmonicity: 3.4
        },
        envelope: {
          attack: 0.01,
          decay: 0.1,
          sustain: 0.5,
          release: 1
        }
      }).toDestination();
    }

    return () => {
      // クリーンアップ
      if (sequence.current) {
        sequence.current.dispose();
      }
      if (synth.current) {
        synth.current.dispose();
      }
    };
  }, []);

  const playChord = (time: number, chord: ProgressionDetail) => {
    if (synth.current && chord.components.length > 0) {
      // 構成音にオクターブを追加（例: C -> C4）
      const notesWithOctave = chord.components.map(note => `${note}4`);
      synth.current.triggerAttackRelease(notesWithOctave, '1n', time);
    }
    // UIの更新をスケジュール
    Tone.Draw.schedule(() => {
      setCurrentChordIndex(progression.indexOf(chord));
    }, time);
  };

  useEffect(() => {
    if (progression.length > 0) {
      if (sequence.current) {
        sequence.current.dispose();
      }
      sequence.current = new Tone.Sequence(playChord, progression, '1n').start(0);
      Tone.Transport.bpm.value = 120;
    }
  }, [progression]);

  const togglePlay = async () => {
    if (Tone.context.state !== 'running') {
      await Tone.start();
    }

    if (isPlaying) {
      Tone.Transport.pause();
      setIsPlaying(false);
    } else {
      Tone.Transport.start();
      setIsPlaying(true);
    }
  };

  const stopPlay = () => {
    Tone.Transport.stop();
    setCurrentChordIndex(-1);
    setIsPlaying(false);
  };

  return (
    <div className="flex items-center space-x-4 p-4 bg-gray-100 rounded-lg">
      <button onClick={togglePlay} className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
        {isPlaying ? 'Pause' : 'Play'}
      </button>
      <button onClick={stopPlay} className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600">
        Stop
      </button>
      <div className="flex-grow flex items-center space-x-2">
        {progression.map((chord, index) => (
          <div key={index} className={`flex-1 h-2 rounded-full ${
            index === currentChordIndex ? 'bg-blue-500' : 'bg-gray-300'
          }`}></div>
        ))}
      </div>
    </div>
  );
};

export default PlaybackControls;