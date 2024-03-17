#!/bin/bash

cd /home/ubuntu/dropord

# Replace the <address> with your specific Bitcoin address
deposit_address=$1
receive_address=$2

amount="0.00001"
FEE=10.0 #Get with `bitcoin-cli estimatefee 1`

date
echo "Watching deposit-address: $deposit_address for $amount and sending to $receive_address"
completefirst=0
completerun=0

while [ $completerun -eq 0 ]; do
  # Check the balance of the Bitcoin deposit-address
  balance=$(bitcoin-cli getreceivedbyaddress $deposit_address)

  # Check if the balance is greater than or equal to the required amount
  if (( $(echo "$balance >= $amount" | bc -l) )); then
    echo "$balance BTC has been deposited into : $deposit_address"

    # When the balance is confirmed, this nft is then moved. If something stuffs up, we can always manually assign
    if [ $completefirst -eq 0 ]; then
      nftfile=$(printf '%s\n' "$(ls -t data/nfts/*.txt | tail -n1)")
      NAME="$(basename $nftfile)"
      mv -v ${nftfile} data/INSCRIBED/${NAME}
      completefirst=1
      echo "${NAME} $deposit_address $receive_address" >> data/owners_pending.txt
    fi

    # Inscribe the file!
    TRANSACTION_INSCRIPTION=$(ord --signet wallet inscribe data/INSCRIBED/${NAME} --fee-rate $FEE --destination $receive_address)
    # Output looks like this:
    # { "commit": "bae9ada5b4d7546fa1a2498fbaa3b594194a8d1a71777fd6912c3574f3836297", "inscription": "5dcb18edeea855b3f06714dd05c551e99e8fff7fbc0e71f2a08483102b648b8ei0", "reveal": "5dcb18edeea855b3f06714dd05c551e99e8fff7fbc0e71f2a08483102b648b8e", "fees": 1168 }

    if [ $? -eq 0 ]; then
      echo "SUCCESS:" $nftfile $TRANSACTION_INSCRIPTION
      TRANSACTION_ID=$(echo $TRANSACTION_INSCRIPTION | jq -r '.commit')
      INSCRIPTION_ID=$(echo $TRANSACTION_INSCRIPTION | jq -r '.inscription')
      echo "$nftfile $deposit_address $receive_address $TRANSACTION_INSCRIPTION" >> data/owners_complete.txt
      completerun=1
      exit

    # IF the Inscription transaction failed for some reason...
    else
      echo FAIL: $TRANSACTION_INSCRIPTION
      echo "Trying again..."
      ## TODO: IF FAILED, must re-run inscription!
    fi

  else
    echo "$balance/$amount BTC confirmed at $address"
  fi

  date
  echo "Sleeping for 60s before getting balance update..."
  sleep 60

done