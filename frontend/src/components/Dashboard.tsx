import React, { useState, useEffect } from 'react';
import {
  Grid,
  Paper,
  Typography,
  TextField,
  Button,
  Card,
  CardContent,
  Box,
  Chip,
  CircularProgress,
  Alert
} from '@mui/material';
import { TrendingUp, TrendingDown, TrendingFlat } from '@mui/icons-material';

const Dashboard: React.FC = () => {
  const [selectedTicker, setSelectedTicker] = useState<string>('AAPL');
  const [prediction, setPrediction] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const popularTickers = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN', 'NVDA', 'META'];

  const fetchPrediction = async () => {
    if (!selectedTicker) return;

    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ticker: selectedTicker }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch prediction');
      }

      const data = await response.json();
      setPrediction(data);

    } catch (err: any) {
      setError(err.message || 'Failed to fetch prediction');
    } finally {
      setLoading(false);
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return <TrendingUp color="success" />;
      case 'down':
        return <TrendingDown color="error" />;
      default:
        return <TrendingFlat color="action" />;
    }
  };

  return (
    <Box>
      <Grid container spacing={3}>
        {/* Stock Selection Panel */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Stock Selection
            </Typography>

            <TextField
              fullWidth
              label="Ticker Symbol"
              value={selectedTicker}
              onChange={(e) => setSelectedTicker(e.target.value.toUpperCase())}
              margin="normal"
              placeholder="e.g., AAPL"
            />

            <Box sx={{ mt: 2, mb: 2 }}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Popular Stocks:
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {popularTickers.map((ticker) => (
                  <Chip
                    key={ticker}
                    label={ticker}
                    onClick={() => setSelectedTicker(ticker)}
                    color={selectedTicker === ticker ? 'primary' : 'default'}
                    clickable
                  />
                ))}
              </Box>
            </Box>

            <Button
              fullWidth
              variant="contained"
              onClick={fetchPrediction}
              disabled={!selectedTicker || loading}
              sx={{ mt: 2 }}
            >
              {loading ? <CircularProgress size={24} /> : 'Get Prediction'}
            </Button>

            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}
          </Paper>
        </Grid>

        {/* Prediction Display */}
        <Grid item xs={12} md={8}>
          {prediction ? (
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h5" component="div">
                    {prediction.ticker} Prediction
                  </Typography>
                  <Chip 
                    label={prediction.trend?.toUpperCase() || 'UNKNOWN'} 
                    color={prediction.trend === 'up' ? 'success' : prediction.trend === 'down' ? 'error' : 'warning'}
                    size="small"
                  />
                </Box>

                <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
                  {getTrendIcon(prediction.trend)}
                  <Box sx={{ ml: 2 }}>
                    <Typography variant="h3" component="div" color="primary">
                      ${prediction.predicted_price?.toFixed(2) || 'N/A'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Predicted Price
                    </Typography>
                  </Box>
                </Box>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Confidence Level:
                  </Typography>
                  <Typography variant="body2" color="text.primary">
                    {((prediction.confidence || 0) * 100).toFixed(1)}%
                  </Typography>
                </Box>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Expected Change:
                  </Typography>
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      color: (prediction.price_change || 0) >= 0 ? 'success.main' : 'error.main',
                      fontWeight: 'bold'
                    }}
                  >
                    ${(prediction.price_change || 0).toFixed(2)} ({(prediction.price_change_percent || 0).toFixed(2)}%)
                  </Typography>
                </Box>

                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Sentiment Score:
                  </Typography>
                  <Typography 
                    variant="body2"
                    sx={{ 
                      color: (prediction.sentiment_score || 0) > 0 ? 'success.main' : 
                             (prediction.sentiment_score || 0) < 0 ? 'error.main' : 'text.primary'
                    }}
                  >
                    {(prediction.sentiment_score || 0).toFixed(3)}
                  </Typography>
                </Box>

                {prediction.timestamp && (
                  <Typography variant="caption" color="text.secondary" sx={{ mt: 2, display: 'block' }}>
                    Generated: {new Date(prediction.timestamp).toLocaleString()}
                  </Typography>
                )}
              </CardContent>
            </Card>
          ) : (
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="h6" color="text.secondary">
                Select a stock and click "Get Prediction" to see AI-powered price forecasts
              </Typography>
            </Paper>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
