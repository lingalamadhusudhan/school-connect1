import "./App.css";

function App() {
  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>School-Connect</h1>
          <p>School Management System</p>
        </div>
      </header>

      <main className="main">
        <section className="welcome-card">
          <h2>Welcome to School-Connect</h2>

          <p>
            Connect administrators, teachers, parents and students
            through one secure school management platform.
          </p>

          <div className="role-container">
            <div className="role-card">
              <h3>Admin</h3>
              <p>Manage the complete school system.</p>
              <button>Admin Login</button>
            </div>

            <div className="role-card">
              <h3>Teacher</h3>
              <p>Manage classes, students and academic activities.</p>
              <button>Teacher Login</button>
            </div>

            <div className="role-card">
              <h3>Parent</h3>
              <p>Monitor your child's school information.</p>
              <button>Parent Login</button>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;