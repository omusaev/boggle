import React from 'react';
import {Container, List, ListItem} from "@material-ui/core";


class ScoreTable extends React.Component {
    render() {
        const foundWords = this.props.foundWords;
        const finalScore = this.props.finalScore;

        const rows = foundWords.map((word, i) =>
            <ListItem
                key={i}
            >
                {word.word} ({word.score})
            </ListItem>
        );

        return (
            <Container>

                <List>
                    <ListItem
                        key="finalScore"
                    >
                        Score: {finalScore}
                    </ListItem>
                    {rows}
                </List>
            </Container>
        );
    }
}

export default ScoreTable;


