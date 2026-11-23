import { useState, useEffect } from "react";

function Notes({ API_URL, accessToken, refreshToken, setAccessToken, setRefreshToken }) {
  const [notes, setNotes] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [msg, setMsg] = useState("");

  function logout() {
    setAccessToken("");
    setRefreshToken("");
  }

  function getNewToken() {
    fetch(API_URL + "/refresh", {
      method: "POST",
      headers: { "refresh-token": refreshToken },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          logout();
        } else {
          setAccessToken(data.access_token);
        }
      });
  }

// E1  
  function getNotes() {
    fetch(API_URL + "/notes", { headers: { token: accessToken } })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          getNewToken();
        } else {
          setNotes(data);
        if (data.length === 0) {
          setMsg("You have no notes yet.");
        } else {
          setMsg("");
        }
      }
    });
}

  // E2
  function addNote() {
    fetch(API_URL + "/notes", {
      method: "POST",
      headers: { "Content-Type": "application/json", token: accessToken },
      body: JSON.stringify({ title: title, content: content }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.detail) {
          if (typeof data.detail === "string") {
            getNewToken();
            setMsg(" click Add Note again");
          } else {
            setMsg("Title and content cannot be empty");
          }
        } else {
          setTitle("");
          setContent("");
          setMsg("");
          getNotes();
        }
      });
  }

  useEffect(() => {
    getNotes();
  }, [accessToken]);

  return (
    <div>
      <h1>My Notes</h1>
      <button onClick={logout}>Logout</button>
      <p>{msg}</p>

      <h2>Add a note</h2>
      <input placeholder="Title" value={title} onChange={(notes) => setTitle(notes.target.value)} />
      <textarea placeholder="Content" value={content} onChange={(notes) => setContent(notes.target.value)} />
      <button onClick={addNote}>Add Note</button>

      <h2>All notes</h2>
      <ul>
        {notes.map((n) => (
          <li key={n.id}>
            <p>Title: {n.title}</p>
            <p>Content: {n.content}</p>
            <p>Created: {n.created_at}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Notes;