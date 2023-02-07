import _ from 'lodash';
import axios from 'axios';

function App() {
  const post = (content) => {
    axios.post('/api/content', content)
      .then(response => {
        console.log(response.data);
        setSaved(true);
      })
      .catch(error => console.log(error));
  }

  const handleChange = (e) => {
    const newContent = e.target.value;
    setContent(newContent);
    setSaved(false);
    debouncedPost(newContent);
  }

  const handleRestore = () => {
    if (confirm('Are you sure you want to restore the html to default?')) {
      axios.post('/api/restore').then(() => window.location.reload());
    }
  }
 
  return <div>Hello World!</div>
}

export default App;
