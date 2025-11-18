export default [
    {
        files: ['assets/js/**/*.js'],
        languageOptions: {
            ecmaVersion: 2021,
            sourceType: 'script',
            globals: {
                window: 'readonly',
                document: 'readonly',
                console: 'readonly',
                L: 'readonly',
                allEvents: 'readonly',
                config: 'readonly',
                navigator: 'readonly',
                Date: 'readonly',
                Math: 'readonly',
                setTimeout: 'readonly',
                alert: 'readonly'
            }
        },
        rules: {
            'no-unused-vars': 'warn',
            'no-console': 'off',
            'semi': ['error', 'always'],
            'indent': ['error', 4],
            'no-trailing-spaces': 'error',
            'eol-last': ['error', 'always']
        }
    }
];
