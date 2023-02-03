import { useState, useRef, useEffect } from "react";
import _ from 'lodash';
import axios from 'axios';
import CodeEditor from '@uiw/react-textarea-code-editor';

function App() {
  const [content, setContent] = useState(_.unescape(filecontent));
  const [saved, setSaved] = useState(true); 

  const post = (content) => {
    axios.post('/api/content', content)
      .then(response => {
        console.log(response.data);
        setSaved(true);
      })
      .catch(error => console.log(error));
  }

  const debouncedPost = useRef(_.debounce(post, 500)).current;

  const handleChange = (e) => {
    const newContent = e.target.value;
    setContent(newContent);
    setSaved(false);
    debouncedPost(newContent);
  }
 
  // Capture ctrl + s
  useEffect(() => {
    document.addEventListener("keydown", function(event) {
      if ((event.metaKey || event.ctrlKey) && event.keyCode === 83) {
        post(content);
        event.preventDefault();
      }
    });
  }, []);
  
  return <div style={{width: 'calc(100vw - 32px', height: 'calc(100vh - 32px)', margin: 16, position: 'absolute'}}>
      <div style={{width: '100%', maxHeight: 'calc(100% - 64px)', marginBottom: 8}} data-color-mode="light">
        Editing website for {username}
        <CodeEditor
          value={content}
          language="html"
          placeholder="Please enter HTML code."
          onChange={handleChange}
          padding={15}
          style={{
            fontSize: 14,
            backgroundColor: "#f5f5f5",
            fontFamily: 'ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace',
          }}
        />
      </div>
      <span style={{display: 'inline-block'}}>
        {saved ? 'Saved' : 'Editing...'}
      </span>
      <div style={{marginTop: 8}}>
        <button onClick={() => window.location.replace(window.location.origin + '/home/' + username)}>Go to website page</button>
      </div>
    </div>
}

export default App;
