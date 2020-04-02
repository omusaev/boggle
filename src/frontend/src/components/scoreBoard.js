import React from 'react';
import {Box, List, ListItem} from "@material-ui/core";


class ScoreBoard extends React.Component {
    render() {
        const games = this.props.games;

        const rows = games.map((game, i) =>
            <ListItem
                key={i}
            >
                <Box display="flex" justifyContent="left">
                    <Box width={130}>
                        {game.player_name || 'Anonymous'}
                    </Box>
                    <Box>
                        {game.final_score}
                    </Box>
                </Box>
            </ListItem>
        );

        return (
            <Box>
                <List>
                    {rows}
                </List>
            </Box>
        );
    }
}

export default ScoreBoard;


