import React from 'react';
import {Box, List, ListItem} from "@material-ui/core";


class CombinationWords extends React.Component {
    render() {
        const words = this.props.words;

        const rows = words.map((word, i) =>
            <ListItem
                key={i}
            >
                {word.word}
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

export default CombinationWords;


