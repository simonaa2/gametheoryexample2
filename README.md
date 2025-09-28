# Game Theory Examples

An interactive Streamlit application demonstrating fundamental concepts in Game Theory.

## Features

This app provides interactive demonstrations of key game theory concepts:

- **Prisoner's Dilemma** - Explore the classic two-player game with customizable payoffs
- **Nash Equilibrium Calculator** - Find pure and mixed strategy equilibria in 2x2 games  
- **Mixed Strategy Calculator** - Calculate optimal mixed strategies with visualization
- **Evolutionary Game Theory** - Simulate population dynamics and evolutionary stable strategies

## Running the Application

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run Hello.py
```

### Docker

1. Build and run with Docker:
```bash
docker build -t gametheory-app .
docker run -p 8501:8501 gametheory-app
```

### Google Cloud Deployment

This application is optimized for Google Cloud Platform deployment:

- **App Engine**: `./deploy-scripts/deploy-app-engine.sh YOUR_PROJECT_ID`
- **Cloud Run**: `./deploy-scripts/deploy-cloud-run.sh YOUR_PROJECT_ID`
- **CI/CD**: Use `cloudbuild.yaml` for automated deployments

See [DEPLOY.md](DEPLOY.md) for detailed deployment instructions.

## Game Theory Concepts Covered

### Nash Equilibrium
A strategy profile where no player can improve their payoff by unilaterally changing their strategy.

### Mixed Strategies
Randomizing over pure strategies with specific probabilities to optimize expected payoffs.

### Evolutionary Stable Strategy (ESS)
A strategy that, if adopted by the population, cannot be invaded by any alternative strategy.

### Replicator Dynamics
A model of how strategy frequencies evolve in populations based on relative fitness.

## Educational Use

This application is designed for:
- Students learning game theory fundamentals
- Educators teaching strategic decision making
- Researchers exploring game theory applications
- Anyone interested in mathematical modeling of strategic interactions
