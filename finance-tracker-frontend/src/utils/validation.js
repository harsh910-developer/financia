import * as Yup from 'yup';

export const loginSchema = Yup.object().shape({
  email: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  password: Yup.string()
    .min(6, 'Password must be at least 6 characters')
    .required('Password is required'),
});

export const registerSchema = Yup.object().shape({
  name: Yup.string()
    .min(2, 'Name must be at least 2 characters')
    .required('Name is required'),
  email: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  password: Yup.string()
    .min(6, 'Password must be at least 6 characters')
    .required('Password is required'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password'), null], 'Passwords must match')
    .required('Confirm password is required'),
});

export const transactionSchema = Yup.object().shape({
  date: Yup.date()
    .max(new Date(), 'Date cannot be in the future')
    .required('Date is required'),
  type: Yup.string()
    .oneOf(['income', 'expense'], 'Invalid transaction type')
    .required('Transaction type is required'),
  category: Yup.string()
    .required('Category is required'),
  amount: Yup.number()
    .positive('Amount must be positive')
    .required('Amount is required'),
  description: Yup.string()
    .max(200, 'Description must be less than 200 characters'),
}); 