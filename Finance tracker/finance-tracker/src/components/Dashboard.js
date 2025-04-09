import React from 'react';
import { motion } from 'framer-motion';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  useTheme,
  useMediaQuery,
} from '@mui/material';
import {
  AccountBalance,
  TrendingUp,
  Add,
  Logout,
  Menu,
} from '@mui/icons-material';
import TransactionForm from './TransactionForm';
import TransactionList from './TransactionList';
import PredictionsDashboard from './PredictionsDashboard';
import SpendingInsights from './SpendingInsights';

const Dashboard = ({ user, transactions, onLogout, onAddTransaction }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const [showTransactionForm, setShowTransactionForm] = React.useState(false);
  const [error, setError] = React.useState(null);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: 'spring',
        stiffness: 100,
      },
    },
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: theme.palette.background.gradient,
        pt: 4,
        pb: 8,
      }}
    >
      <Container maxWidth="lg">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <Grid container spacing={3}>
            {/* Header */}
            <Grid item xs={12}>
              <motion.div variants={itemVariants}>
                <Card>
                  <CardContent sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <AccountBalance sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
                      <Box>
                        <Typography variant="h5" component="h1">
                          Welcome, {user.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Track your expenses and get insights
                        </Typography>
                      </Box>
                    </Box>
                    <Box>
                      <IconButton onClick={onLogout} color="primary">
                        <Logout />
                      </IconButton>
                    </Box>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>

            {/* Quick Stats */}
            <Grid item xs={12} md={4}>
              <motion.div variants={itemVariants}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Total Balance
                    </Typography>
                    <Typography variant="h4" color="primary.main">
                      ${transactions.reduce((acc, curr) => acc + curr.amount, 0).toFixed(2)}
                    </Typography>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>

            <Grid item xs={12} md={4}>
              <motion.div variants={itemVariants}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Monthly Spending
                    </Typography>
                    <Typography variant="h4" color="secondary.main">
                      ${transactions
                        .filter(t => new Date(t.date).getMonth() === new Date().getMonth())
                        .reduce((acc, curr) => acc + curr.amount, 0)
                        .toFixed(2)}
                    </Typography>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>

            <Grid item xs={12} md={4}>
              <motion.div variants={itemVariants}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Savings Rate
                    </Typography>
                    <Typography variant="h4" color="success.main">
                      {((transactions.reduce((acc, curr) => acc + curr.amount, 0) /
                        transactions.filter(t => new Date(t.date).getMonth() === new Date().getMonth())
                          .reduce((acc, curr) => acc + curr.amount, 0)) *
                        100).toFixed(1)}%
                    </Typography>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>

            {/* Main Content */}
            <Grid item xs={12} md={8}>
              <motion.div variants={itemVariants}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                      <Typography variant="h6">Recent Transactions</Typography>
                      <Button
                        variant="contained"
                        startIcon={<Add />}
                        onClick={() => setShowTransactionForm(true)}
                      >
                        Add Transaction
                      </Button>
                    </Box>
                    <TransactionList transactions={transactions} />
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>

            <Grid item xs={12} md={4}>
              <motion.div variants={itemVariants}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Spending Insights
                    </Typography>
                    <SpendingInsights transactions={transactions} />
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          </Grid>
        </motion.div>
      </Container>

      {showTransactionForm && (
        <TransactionForm
          open={showTransactionForm}
          onClose={() => setShowTransactionForm(false)}
          onSubmit={onAddTransaction}
        />
      )}
    </Box>
  );
};

export default Dashboard; 