import React from 'react';
import { useLocation } from 'react-router-dom';
import {
  Box,
  Tabs,
  Tab,
  Container
} from '@mui/material';
import { Dashboard } from '@mui/icons-material';

const Navigation: React.FC = () => {
  const location = useLocation();

  const getTabValue = () => {
    if (location.pathname === '/') return 0;
    return 0;
  };

  return (
    <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
      <Container maxWidth="xl">
        <Tabs value={getTabValue()} aria-label="navigation tabs">
          <Tab
            icon={<Dashboard />}
            label="Dashboard"
          />
        </Tabs>
      </Container>
    </Box>
  );
};

export default Navigation;
