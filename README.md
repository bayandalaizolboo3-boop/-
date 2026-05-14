# <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>React Tetris</title>
  <link rel="stylesheet" href="style.css">
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap" rel="stylesheet">
  
  <!-- React via CDN -->
  <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
  
  <!-- Babel for parsing JSX -->
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
const { useState, useEffect, useCallback, useRef } = React;

// Constants & Helpers
const STAGE_WIDTH = 10;
const STAGE_HEIGHT = 20;

const TETROMINOS = {
  0: { shape: [[0]], color: 'rgba(0,0,0,0)' },
  I: { shape: [[0,0,0,0], ['I','I','I','I'], [0,0,0,0], [0,0,0,0]], color: '#00ffff' },
  J: { shape: [['J',0,0], ['J','J','J'], [0,0,0]], color: '#0000ff' },
  L: { shape: [[0,0,'L'], ['L','L','L'], [0,0,0]], color: '#ffa500' },
  O: { shape: [['O','O'], ['O','O']], color: '#ffff00' },
  S: { shape: [[0,'S','S'], ['S','S',0], [0,0,0]], color: '#00ff00' },
  T: { shape: [[0,'T',0], ['T','T','T'], [0,0,0]], color: '#800080' },
  Z: { shape: [['Z','Z',0], [0,'Z','Z'], [0,0,0]], color: '#ff0000' }
};

const randomTetromino = () => {
  const tetrominos = 'IJLOSTZ';
  const randTetromino = tetrominos[Math.floor(Math.random() * tetrominos.length)];
  return { type: randTetromino, ...TETROMINOS[randTetromino] };
};

const createStage = () =>
  Array.from(Array(STAGE_HEIGHT), () => new Array(STAGE_WIDTH).fill([0, 'clear']));

const checkCollision = (player, stage, { x: moveX, y: moveY }) => {
  for (let y = 0; y < player.tetromino.length; y += 1) {
    for (let x = 0; x < player.tetromino[y].length; x += 1) {
      if (player.tetromino[y][x] !== 0) {
        if (
          !stage[y + player.pos.y + moveY] ||
          !stage[y + player.pos.y + moveY][x + player.pos.x + moveX] ||
          stage[y + player.pos.y + moveY][x + player.pos.x + moveX][1] !== 'clear'
        ) {
          return true;
        }
      }
    }
  }
  return false;
};

// Hook: useInterval
function useInterval(callback, delay) {
  const savedCallback = useRef();
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);
  useEffect(() => {
    function tick() {
      savedCallback.current();
    }
    if (delay !== null) {
      const id = setInterval(tick, delay);
      return () => {
        clearInterval(id);
      };
    }
  }, [delay]);
}

const App = () => {
  const [dropTime, setDropTime] = useState(null);
  const [gameOver, setGameOver] = useState(false);
  
  const [player, setPlayer] = useState({
    pos: { x: 0, y: 0 },
    tetromino: TETROMINOS[0].shape,
    collided: false,
  });

  const [stage, setStage] = useState(createStage());
  
  const [score, setScore] = useState(0);
  const [rows, setRows] = useState(0);
  const [level, setLevel] = useState(1);
  const [gameStarted, setGameStarted] = useState(false);

  const resetPlayer = useCallback(() => {
    setPlayer({
      pos: { x: STAGE_WIDTH / 2 - 2, y: 0 },
      tetromino: randomTetromino().shape,
      collided: false,
    });
  }, []);

  useEffect(() => {
    if (!gameStarted) return;

    const sweepRows = newStage => {
      let rowsCleared = 0;
      const sweptStage = newStage.reduce((ack, row) => {
        if (row.findIndex(cell => cell[0] === 0) === -1) {
          rowsCleared += 1;
          ack.unshift(new Array(STAGE_WIDTH).fill([0, 'clear']));
          return ack;
        }
        ack.push(row);
        return ack;
      }, []);
      if (rowsCleared > 0) {
         setScore(prev => prev + [0, 40, 100, 300, 1200][rowsCleared] * level);
         setRows(prev => prev + rowsCleared);
      }
      return sweptStage;
    };

    const updateStage = prevStage => {
      const newStage = prevStage.map(row =>
        row.map(cell => (cell[1] === 'clear' ? [0, 'clear'] : cell))
      );

      player.tetromino.forEach((row, y) => {
        row.forEach((value, x) => {
          if (value !== 0) {
            newStage[y + player.pos.y][x + player.pos.x] = [
              value,
              `${player.collided ? 'merged' : 'clear'}`,
            ];
          }
        });
      });

      if (player.collided) {
        resetPlayer();
        return sweepRows(newStage);
      }
      return newStage;
    };

    setStage(prev => updateStage(prev));
  }, [player, resetPlayer, level, gameStarted]);

  const movePlayer = dir => {
    if (!checkCollision(player, stage, { x: dir, y: 0 })) {
      setPlayer(prev => ({ ...prev, pos: { x: prev.pos.x + dir, y: prev.pos.y }}));
    }
  };

  const startGame = () => {
    setStage(createStage());
    setDropTime(1000);
    resetPlayer();
    setGameOver(false);
    setScore(0);
    setRows(0);
    setLevel(1);
    setGameStarted(true);
  };

  const drop = () => {
    if (rows > level * 10) {
      setLevel(prev => prev + 1);
      setDropTime(1000 / level + 200);
    }
    if (!checkCollision(player, stage, { x: 0, y: 1 })) {
      setPlayer(prev => ({ ...prev, pos: { x: prev.pos.x, y: prev.pos.y + 1 }}));
    } else {
      if (player.pos.y < 1) {
        setGameOver(true);
        setDropTime(null);
      }
      setPlayer(prev => ({ ...prev, collided: true }));
    }
  };

  const keyUp = ({ keyCode }) => {
    if (!gameOver && gameStarted) {
      if (keyCode === 40) {
        setDropTime(1000 / level + 200);
      }
    }
  };

  const dropPlayer = () => {
    setDropTime(null);
    drop();
  };

  const rotate = (matrix, dir) => {
    const rotatedTetro = matrix.map((_, index) => matrix.map(col => col[index]));
    if (dir > 0) return rotatedTetro.map(row => row.reverse());
    return rotatedTetro.reverse();
  };

  const playerRotate = (stage, dir) => {
    const clonedPlayer = JSON.parse(JSON.stringify(player));
    clonedPlayer.tetromino = rotate(clonedPlayer.tetromino, dir);

    const pos = clonedPlayer.pos.x;
    let offset = 1;
    while (checkCollision(clonedPlayer, stage, { x: 0, y: 0 })) {
      clonedPlayer.pos.x += offset;
      offset = -(offset + (offset > 0 ? 1 : -1));
      if (offset > clonedPlayer.tetromino[0].length) {
        rotate(clonedPlayer.tetromino, -dir);
        clonedPlayer.pos.x = pos;
        return;
      }
    }
    setPlayer(clonedPlayer);
  };

  const move = (e) => {
    if (!gameOver && gameStarted) {
      // Prevent default scrolling
      if([37, 38, 39, 40].indexOf(e.keyCode) > -1) {
        e.preventDefault();
      }
      if (e.keyCode === 37) {
        movePlayer(-1);
      } else if (e.keyCode === 39) {
        movePlayer(1);
      } else if (e.keyCode === 40) {
        dropPlayer();
      } else if (e.keyCode === 38) {
        playerRotate(stage, 1);
      }
    }
  };

  useInterval(() => {
    drop();
  }, dropTime);

  // Focus wrapper to capture keyboard events
  const wrapperRef = useRef(null);
  useEffect(() => {
      if(wrapperRef.current) {
          wrapperRef.current.focus();
      }
  }, [gameStarted]);

  return (
    <div 
        className="game-wrapper" 
        role="button" 
        tabIndex="0" 
        onKeyDown={move} 
        onKeyUp={keyUp}
        ref={wrapperRef}
    >
      <div className="game-container">
        <div className="stage">
          {stage.map(row => row.map((cell, x) => (
            <div 
              key={x} 
              className="cell" 
              style={{
                 backgroundColor: cell[0] === 0 ? 'rgba(0,0,0,0.5)' : TETROMINOS[cell[0]].color,
                 border: cell[0] === 0 ? '1px solid rgba(255,255,255,0.05)' : '1px solid rgba(255,255,255,0.5)',
                 boxShadow: cell[0] === 0 ? 'none' : `inset 0 0 10px rgba(255,255,255,0.3), 0 0 15px ${TETROMINOS[cell[0]].color}`
              }}
            />
          )))}
        </div>
        <aside className="side-panel">
          {gameOver ? (
            <div className="display-box game-over">Game Over!</div>
          ) : (
            <>
              <div className="display-box">
                  <div className="display-title">Score</div>
                  <div className="display-value">{score}</div>
              </div>
              <div className="display-box">
                  <div className="display-title">Level</div>
                  <div className="display-value">{level}</div>
              </div>
              <div className="display-box">
                  <div className="display-title">Rows</div>
                  <div className="display-value">{rows}</div>
              </div>
            </>
          )}
          <button className="start-button" onClick={() => { startGame(); wrapperRef.current?.focus(); }}>
            {gameOver ? 'Play Again' : gameStarted ? 'Restart' : 'Start Game'}
          </button>
          
          <div className="instructions">
            <h3>Controls</h3>
            <p>↑ : Rotate</p>
            <p>← → : Move</p>
            <p>↓ : Drop</p>
          </div>
        </aside>
      </div>
    </div>
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
  </script>
</body>
</html>
