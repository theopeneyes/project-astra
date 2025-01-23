import React from 'react';

const PageNotFound = () => {
  const styles = {
    pageContainer: {
      padding: '40px 0',
      background: '#fff',
      fontFamily: "'Arvo', serif",
    },
    fourZeroFourBg: {
      backgroundImage: 'url(https://cdn.dribbble.com/users/285475/screenshots/2083086/dribbble_1.gif)',
      height: '400px',
      backgroundPosition: 'center',
      textAlign: 'center',
    },
    fourZeroFourText: {
      fontSize: '80px',
    },
    contentBox: {
      marginTop: '-50px',
      textAlign: 'center',
    },
    heading: {
      fontSize: '30px',
    },
    link404: {
      color: '#fff',
      padding: '10px 20px',
      backgroundColor: '#39ac31',
      margin: '20px 0',
      display: 'inline-block',
      textDecoration: 'none',
      borderRadius: '5px',
    },
  };

  return (
    <div style={styles.pageContainer}>
      <div className="container">
        <div className="row">
          <div className="col-sm-12">
            <div className="col-sm-10 col-sm-offset-1 text-center">
              <div style={styles.fourZeroFourBg}>
                <h1 style={styles.fourZeroFourText}>404</h1>
              </div>
              <div style={styles.contentBox}>
                <h3 style={styles.heading}>Look like you're lost</h3>
                <p>The page you are looking for is not available!</p>
                <a href="/" style={styles.link404}>Go to Home</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PageNotFound;
