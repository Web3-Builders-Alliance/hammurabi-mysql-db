# Hammurabi Orca Database

This repository hosts a comprehensive database of transaction data for the SOL-USDC pool on Orca, one of the leading decentralized exchanges on the Solana blockchain. Our dataset includes detailed information on each transaction, providing valuable insights for traders, analysts, and enthusiasts. 

The eventual aim is to expand the database to feature comprehensive coverage of Orca liquidity pool data and eventually provide coverage of additional decentralized exchanges on Solana such as Raydium. However this codebase is still a work in progress. 

## Setup 

**Python**

To use this repository, you'll need Python 3.9 and the necessary libraries installed on your local machine. Follow these steps for Mac and Linux systems:

### Installing Python 3.9

#### For Mac Users:
1. You can install Python 3.9 using Homebrew, a package manager for Mac. If you don't have Homebrew installed, visit [brew.sh](https://brew.sh) to install it. Then, run the following command:
   ```brew install python@3.9```

2. After installation, ensure that Python 3.9 is the default version: 
``brew link python@3.9 --force --overwrite``

#### For Linux Users: 
1. On Linux, you can install Python 3.9 using the package manager. For Debian-based systems like Ubuntu, use: 
``sudo apt-get update
sudo apt-get install python3.9``

### Installing Dependencies from `requirements.txt`

1. Clone the repository and navigate to the folder: 
``git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name``

2. Install the required Python packages using: 
``pip3 install -r requirements.txt``

Now, you are all set up to run and modify the project on your local machine. 

**Cloudflare R2**

Cloudflare R2 is a cloud storage solution that offers a free tier for users. To sign up for your own free R2 bucket, follow these simple steps:

1. **Create a Cloudflare Account:**
   - Visit the [Cloudflare website](https://www.cloudflare.com/).
   - Click on the 'Sign Up' button and follow the instructions to create a new account.

2. **Access the Cloudflare Dashboard:**
   - Once your account is set up, log in and navigate to the Cloudflare dashboard.

3. **Navigate to R2 Storage:**
   - In the dashboard, look for the 'R2 Storage' option, typically found under the 'Storage' section.

4. **Create a New R2 Bucket:**
   - Click on 'Create Bucket' or a similar option to initiate the process.
   - Follow the on-screen instructions to name and configure your R2 bucket.

5. **Review and Complete:**
   - Review your bucket settings and confirm the creation of your new R2 bucket.

Once your R2 bucket is created, you can start using it for storage purposes immediately. Remember, Cloudflare R2 offers a generous free tier, but it's important to be aware of any limitations or charges that may apply beyond the free tier usage.

**Flipside Crypto**

To access the Flipside Crypto dataset, you will need an API key. To obtain an API key, sign up for the app and navigate to the key management page.

Alternatively, you can visit app.flipsidecrypto.com and sign up for an account using either your Discord, ETH wallet, or email. Write your query in the application's query editor, set an appropriate refresh rate in the upper right corner, and use the API button to generate a URL. Use this URL as a GET request in your code, and the Python json library to parse the query results.

## Architecture 

## Data Schema

## Contributions

Contributions of any form are encouraged and appreciated. Please follow the "fork and pull" Git workflow if you would like to create a new feature:

  1. Fork the repo on Github
  2. Clone the repo onto your own machine
  3. Create a new branch and commit any changes to this branch
  4. Push your work to back up your fork
  5. Submit a pull request and request review from jhuhnke
IMPORTANT: Be sure to merge the lastest commit from upstream before submitting a pull request.

The more detailed the branch name and description of the pull request, the better! A thorough description of what you are adding to the codebase will help speed up the review process.

To report a bug or submit a feature request, please use the issues tab to open and submit an issue. The more detailed the bug report or feature request, the easier it is for me to integrate it into the application!

## Donations 

Any donations are greatly appreciated and will be put torwards the cost of the database. Extra donations will likely be used to buy the dev a coffee or a beer.

Solana address: 2L6j3wZXEByg8jycytabZitDh9VVMhKiMYv7EeJh6R2H

## License 

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any queries or suggestions, please reach out to me via email at huhnkejessica@gmail.com or on X: @web3_analyst

