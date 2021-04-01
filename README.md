# flight-deals
Udemy "100 Days of Python", Day 39 Project:  Flight Deal Tracker

Reads a Google Sheet containing flight destinations and a low fare trigger price.  

For each destination, uses the Kiwi.com Tequila API to find flight prices.  If a
flight price is lower than the trigger price, sends an SMS message via Twilio with
the fight information.
