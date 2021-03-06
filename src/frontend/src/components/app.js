import React from 'react';
import {
    Box, Container, Divider,
    ExpansionPanel, ExpansionPanelSummary, ExpansionPanelDetails,
    Typography
} from "@material-ui/core";


import '../styles/app.css';

import apiClient from "../core/apiClient";
import settings from '../conf/settings'

import GameStart from './gameStart';
import Game from './game';
import ShareGameLink from './shareGameLink';
import ScoreBoard from './scoreBoard';
import CombinationWords from './combinationWords';


class App extends React.Component {
    constructor(props) {
        super(props);

        this.gameTtl = settings.gameTtl;
        this.siteUrl = settings.siteUrl;
        this.combinationIdParam = 'c';

        this.errorMessages = {
            'COMBINATION_DOES_NOT_EXIST': 'The combination does not exist',
            'GAME_DOES_NOT_EXIST': 'The game does not exist',
            'GAME_IS_FINISHED': 'The game is finished',
            'WORD_HAS_BEEN_ADDED_ALREADY': 'Got it already!',
            'INCORRECT_LENGTH': 'Minimum length is 3 letters!',
            'INCORRECT_SEQUENCE': 'Hmm, don\'t see it on the board',
            'WORD_DOES_NOT_EXIST': 'The word does not exist!',
        };

        const urlParams = new URLSearchParams(props.location.search);
        const combination_id = urlParams.get(this.combinationIdParam);

        this.state = {
            gameInProcess: false,
            gameFinished: false,
            playerName: '',
            isChallenge: !!combination_id,
            combinationId: combination_id,
            shareLink: '',
            gameId: '',
            letters: [],
            foundWords: [],
            combinationWords: [],
            finalScore: 0,
            time: {
                minutes: 0,
                seconds: 0
            },
            secondsLeft: 0,
            currentWord: '',
            message: {
                isError: false,
                text: ''
            },
            scoreBoard: []
        };

        this.timer = 0;

        this.updatePlayerName = this.updatePlayerName.bind(this);
        this.updateCurrentWord = this.updateCurrentWord.bind(this);
        this.handleGameStart = this.handleGameStart.bind(this);
        this.handleNewWord = this.handleNewWord.bind(this);
        this.countDown = this.countDown.bind(this);
        this.startTimer = this.startTimer.bind(this);
        this.onDiceClick = this.onDiceClick.bind(this);
    }

    updatePlayerName(event) {
        this.setState({
            playerName: event.target.value
        })
    }

    updateCurrentWord(event) {
        this.setState({
            currentWord: event.target.value.toUpperCase()
        })
    }

    onDiceClick(letter) {
        this.setState({
            currentWord: this.state.currentWord + letter
        })
    }

    startTimer() {
        if (this.timer === 0) {
            this.timer = setInterval(this.countDown, 1000);
        }
    }

    countDown() {
        let seconds = this.state.secondsLeft - 1;
        this.setState({
            time: this.secondsToTime(seconds),
            secondsLeft: seconds,
        });

        if (seconds === 0) {
            clearInterval(this.timer);
            this.timer = 0;

            this.finishGame();
        }
    }

    secondsToTime(secs) {
        const minutes = Math.floor(secs / 60);
        const seconds = Math.ceil(secs % 60);

        const time = {
            minutes: minutes,
            seconds: seconds
        };

        return time;
    }

    finishGame() {
        const combinationId = this.state.combinationId;

        this.setState({
            gameInProcess: false,
            gameFinished: true,
            currentWord: '',
            message: {
                isError: false,
                text: "Time's up!"
            }
        });

        const params = {
            'combination_id': combinationId
        };

        apiClient(
            {
                method: 'get',
                path: 'games',
                params: params
            }
        )
            .then(response => {
                const data = response.data;

                this.setState({
                    scoreBoard: data.games
                });
            })

        apiClient(
            {
                method: 'get',
                path:  `combinations/${combinationId}`,
            }
        )
            .then(response => {
                const data = response.data;

                this.setState({
                    combinationWords: data.words
                });
            })
    }

    buildShareLink(combinationId) {
        return `${this.siteUrl}?${this.combinationIdParam}=${combinationId}`
    }

    handleGameStart(acceptChallenge) {
        const combinationId = this.state.combinationId;
        const playerName = this.state.playerName;

        let data = {
            player_name: playerName
        };

        if (acceptChallenge) {
            data['combination_id'] = combinationId
        }

        apiClient({
            method: 'post',
            path: 'games',
            data: data
        })
            .then(response => {
                const data = response.data;

                const shareLink = this.buildShareLink(data.combination_id);

                this.setState({
                    secondsLeft: this.gameTtl,
                    gameInProcess: true,
                    gameFinished: false,
                    combinationId: data.combination_id,
                    gameId: data.id,
                    letters: data.letters,
                    foundWords: data.found_words,
                    finalScore: data.final_score,
                    shareLink: shareLink,
                    message: {
                        isError: false,
                        text: "Good luck!"
                    }
                });

                this.startTimer();

            })
            .catch(error => {
                // shouldn't happen in the positive scenario
                console.log(error);
            });
    }

    handleNewWord() {
        const gameId = this.state.gameId;
        const currentWord = this.state.currentWord;

        const data = {
            word: currentWord
        };

        apiClient({
            method: 'post',
            path: `games/${gameId}`,
            data: data
        })
            .then(response => {
                const data = response.data;

                this.setState({
                    currentWord: '',
                    foundWords: data.found_words,
                    finalScore: data.final_score,
                    message: {
                        isError: false,
                        text: 'Nice catch!'
                    }
                })
            })
            .catch(error => {
                const data = error.response.data;
                this.setState({
                    message: {
                        isError: true,
                        text: this.errorMessages[data.error_code] || data.error_message
                    },
                    currentWord: ''
                })
            });
    }

    render() {
        const isChallenge = this.state.isChallenge;
        const shareLink = this.state.shareLink;
        const gameInProcess = this.state.gameInProcess;
        const gameFinished = this.state.gameFinished;
        const letters = this.state.letters;
        const time = this.state.time;
        const foundWords = this.state.foundWords;
        const finalScore = this.state.finalScore;
        const message = this.state.message;
        const currentWord = this.state.currentWord;
        const scoreBoard = this.state.scoreBoard;
        const combinationWords = this.state.combinationWords;

        return (
            <Container maxWidth="sm">
                <Box pt={5}>
                    <Box pb={2}>
                        <GameStart
                            gameInProcess={gameInProcess}
                            isChallenge={isChallenge}
                            onStartGame={this.handleGameStart}
                            onPlayerNameUpdate={this.updatePlayerName}
                        />
                    </Box>
                    {(gameFinished || gameInProcess) &&
                    <Divider variant="middle"/>}
                    <Box pt={2}>
                        {(gameFinished || gameInProcess) && <Game
                            gameInProcess={gameInProcess}
                            letters={letters}
                            time={time}
                            foundWords={foundWords}
                            finalScore={finalScore}
                            onCurrentWordUpdate={this.updateCurrentWord}
                            onNewWordSubmit={this.handleNewWord}
                            message={message}
                            currentWord={currentWord}
                            onDiceClick={this.onDiceClick}
                        />
                        }
                    </Box>
                    {gameFinished && <Divider variant="middle"/>}
                    {gameFinished &&
                    <Box display="flex" justifyContent="center" pt={2} pb={2}>
                        <Box>
                            <ExpansionPanel>
                                <ExpansionPanelSummary
                                    aria-controls="scoreboard-content"
                                    id="scoreboard-header"
                                >
                                    <Typography>Score Board</Typography>
                                </ExpansionPanelSummary>
                                <ExpansionPanelDetails>
                                    <ScoreBoard
                                        games={scoreBoard}
                                    />
                                </ExpansionPanelDetails>
                            </ExpansionPanel>
                            <ExpansionPanel>
                                <ExpansionPanelSummary
                                    aria-controls="allwords-content"
                                    id="allwords-header"
                                >
                                    <Typography>All possible words</Typography>
                                </ExpansionPanelSummary>
                                <ExpansionPanelDetails>
                                    <CombinationWords
                                        words={combinationWords}
                                    />
                                </ExpansionPanelDetails>
                            </ExpansionPanel>
                        </Box>
                    </Box>
                    }
                    {(gameFinished || gameInProcess) &&
                    <Divider variant="middle"/>}
                    <Box display="flex" justifyContent="center" pt={2}>
                        <Box width={1 / 2}>
                            <ShareGameLink
                                shareLink={shareLink}
                            />
                        </Box>
                    </Box>
                </Box>
            </Container>
        );
    }
}

export default App;
