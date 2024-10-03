import { useState } from 'react';
import './App.css';
import { useSpeechSynthesis } from 'react-speech-kit';


function App() {
  const { speak } = useSpeechSynthesis();
  const [inputText, setinputText] = useState('');

  function handleSpeak(){
    speak({text:inputText,rate:0.5})

  }
return (
  <>
    <h2>SightSense-Navigation System for Visually impaired</h2>
    <textarea rows='5' cols='50' placeholder='Alert!' onChange={(e) => setinputText(e.target.value)} />
    <br />
    <button onClick={handleSpeak}>Speak</button>
  </>
);
}

export default App;