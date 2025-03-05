import React, { useState } from 'react';

export default function Registration() {
  const [formData, setFormData] = useState({
    name: 'Jiara Martins',
    email: 'hello@reallygreatsite.com',
    dateOfBirth: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
  };

  const handleFaceScan = () => {
    console.log('Face scan initiated');
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100vw',
      height: '100vh',
      backgroundColor: 'black',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '1rem',
      boxSizing: 'border-box'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '400px'
      }}>
        <h2 style={{
          color: 'white',
          fontSize: '2rem',
          fontWeight: 'bold',
          textAlign: 'center',
          marginBottom: '2rem'
        }}>
          Create new Account
        </h2>
        <p style={{
          color: 'gray',
          textAlign: 'center',
          marginBottom: '1rem'
        }}>
          Already Registered? <a href="/login" style={{ color: 'white', textDecoration: 'underline' }}>Login</a>
        </p>
        
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <input 
            type="text" 
            name="name"
            value={formData.name}
            onChange={handleChange}
            style={{
              width: '100%',
              padding: '0.5rem',
              backgroundColor: 'transparent',
              border: '1px solid gray',
              color: 'white',
              outline: 'none'
            }}
          />
          
          <input 
            type="email" 
            name="email"
            value={formData.email}
            onChange={handleChange}
            style={{
              width: '100%',
              padding: '0.5rem',
              backgroundColor: 'transparent',
              border: '1px solid gray',
              color: 'white',
              outline: 'none'
            }}
          />
          
          <select 
            name="dateOfBirth"
            value={formData.dateOfBirth}
            onChange={handleChange}
            style={{
              width: '100%',
              padding: '0.5rem',
              backgroundColor: 'black',
              border: '1px solid gray',
              color: 'white',
              outline: 'none'
            }}
          >
            <option value="">Select</option>
          </select>
          
          <button 
            type="submit"
            style={{
              width: '100%',
              padding: '0.5rem',
              backgroundColor: 'white',
              color: 'black',
              fontWeight: 'bold',
              textTransform: 'uppercase',
              border: 'none',
              cursor: 'pointer'
            }}
          >
            sign up
          </button>
        </form>
        
        <div 
          onClick={handleFaceScan}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginTop: '1.5rem',
            cursor: 'pointer'
          }}
        >
          <div style={{ 
            width: '48px', 
            height: '48px', 
            backgroundColor: 'transparent', 
            border: '2px solid #39FF14', 
            borderRadius: '50%',
            marginRight: '1rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <div style={{
              width: '24px',
              height: '24px',
              backgroundColor: '#39FF14',
              borderRadius: '50%'
            }}></div>
          </div>
          <span style={{
            color: 'white',
            textTransform: 'uppercase',
            letterSpacing: '0.05em'
          }}>
            Click to Scan Your Face
          </span>
        </div>
      </div>
    </div>
  );
}