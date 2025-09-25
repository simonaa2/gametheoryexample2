# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Game Theory Applications",
        page_icon="🎮",
    )

    st.write("# Game Theory Applications 🎮")

    st.sidebar.success("Select a game theory application above.")

    st.markdown(
        """
        Welcome to our interactive Game Theory Applications!
        
        This application provides tools to analyze and understand various concepts in game theory.
        **👈 Select an application from the sidebar** to explore different game theory scenarios:
        
        ### Available Applications:
        - **Nash Equilibrium Calculator** - Find Nash equilibria in strategic form games
        - **Prisoner's Dilemma** - Interactive prisoner's dilemma game simulation
        - **Strategic Form Games** - Analyze payoff matrices and dominant strategies
        - **Mixed Strategy Calculator** - Calculate optimal mixed strategies
        
        ### About Game Theory:
        Game theory is the mathematical study of strategic decision making among rational agents. 
        It provides tools for understanding situations where the outcome for each participant 
        depends on the actions of all participants.
        
        ### Key Concepts:
        - **Nash Equilibrium**: A strategy profile where no player can improve by unilaterally changing strategy
        - **Dominant Strategy**: A strategy that is optimal regardless of what other players do
        - **Payoff Matrix**: A table showing the outcomes for different strategy combinations
        - **Mixed Strategy**: A probability distribution over pure strategies
    """
    )


if __name__ == "__main__":
    run()
