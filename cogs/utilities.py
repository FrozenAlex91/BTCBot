import discord
from discord.ext import commands
import requests
import json
import os
from dotenv import load_dotenv

class Utilities(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# Report to r/bitcoin mod-log. Subsitute other channel ID's as necessary
	#todo get channel by ID
	@commands.command()
	async def report(self, ctx):
		load_dotenv()
		if os.getenv('ENABLE_REPORTS') == "1":
			reportChannel = os.getenv('REPORT_CHANNEL')
			for guild in self.bot.guilds:
				for channel in guild.channels:
					if channel.name == reportChannel:
						msg = ctx.author.mention + " reporting: " + ctx.message.content.replace("!report ", "")
						if ctx.message.reference is not None:
							reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
							msg += " - " + reply.author.mention + ": " + reply.content + " - " + reply.jump_url
						await channel.send(msg);

			await ctx.message.delete()


	@commands.command()
	async def newuser(self, ctx):
		if ctx.message.reference is not None:
			reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
			user = ", " + reply.author.mention
		else:
			user = ""
		await ctx.channel.send("Welcome to the r/Bitcoin chat" + user + ". Please review the #rules while you're here; primarily no altcoin, stock, or off topic discussion. Also please read our newcomers faq at https://www.reddit.com/r/Bitcoin/comments/i19uta/bitcoin_newcomers_faq_please_read/. For additional learning resources and information please check out https://lopp.net/bitcoin.html, a community curated resource list. To report users for breaking these rules please reply to the rulebreaking comment and type !report <reason>.")

	
	@commands.command()
	async def exchanges(self, ctx, *args):
		exchangeDic = {
			"international": "Bitstamp, Coinbase, Gemini, Kraken, OKCoin, Binance",
			"p2p": "Bisq, HodlHodl, BitQuickBitcoin, Local Bitcoins, PaxfulBitcoin",
			"bahrain": "Rain",
			"indonesia":"Indodax",
			"israel": "Bits of Gold",
			"japan": "Bitbank, BitFlyer ,BtcBox",
			"kuwait": "Rain",
			"malaysia": "Luno",
			"oman": "Rain",
			"singapore": "Binance, Mine Digital",
			"south korea":"Bithumb , Coinone, Korbit",
			"saudi arabia":"Rain",
			"taiwan": "MaiCoin MAX, BitoPro",
			"turkey": "Koinim",
			"uae": "BitOasis, Karsha, Rain",
			"europe""": "Kraken, Coinbase, AnyCoin Direct, Binance, Bitcoin.de, bitFlyer, BitPanda, Bitvavo, Kriptomat, Paymium, The Rock Trading",
			"netherlands": "Bitvavo",
			"poland": "BitBay",
			"ukraine": "Kuna",
			"uk": "Binance, Bittylicious, CoinCorner, Coinfloor",
			"nigeria": "Luno, BuyCoins",
			"south africa": "Luno",
			"uganda": "Binance",
			"canada": "BullBitcoin, Newton, Kraken, Shakepay, Bitbuy, Canadian Bitcoins, Coinberry, Coinsmart",
			"mexico": "Bitso, Volabit",
			"usa": "Kraken, Coinbase, CEX IO, Bitstamp, bitFlyer, Bittrex, Gemini, itBit, River Financial, Swan Bitcoin, eToro, Binance, LocalBitcoins, Changelly, Coinmama, Bitpanda, Blockchain, BitcoinIRA, CoinSwitch, KuCoin, CashApp, Bisq, Paxful",
			"argentina": "ArgenBTC, SatoshiTango",
			"brazil": "Brasil Bitcoin, Mercado Bitcoin, NovaDAX, Walltime",
			"chile": "Buda",
			"colombia": "Buda",
			"peru": "Buda",
			"venezuela": "Bisq, Cryptobuyer",
			"australia": "Bitaroo, BTC Markets, CoinJar, CoinSpot, Digital Surge, CoinTree, HardBlock, Independent Reserve, Mine Digital, Swyftx",
			"new zealand": "Independent Reserve, Kiwi-coin, Mine Digital"
			}
		arg = ""
		for a in args[0]:
			arg += str(a) + " "
		arg = arg[0:len(arg)-1]
		if arg.lower() in exchangeDic:
			await ctx.channel.send("Exchanges in " + arg + ": " + exchangeDic[arg.lower()])
		else:
			keys = ""
			for k in exchangeDic.keys():
				keys += k + ", "
			keys = keys[0:len(keys)-2]
			await ctx.channel.send("Available options: " + keys)

	@commands.command()
	async def exchange(self, ctx, *args):
		await Utilities(self).exchanges(self, ctx, args)

	@commands.command()
	async def ex(self, ctx, *args):
		await Utilities(self).exchanges(self, ctx, args)

	@commands.command()
	async def x(self, ctx, *args):
		await Utilities(self).exchanges(self, ctx, args)

	@commands.command()
	async def wallets(self, ctx, *args):
		walletDic = {
			"electrum": {"tags": ["pc", "windows", "linux", "mac", "ios", "android", "hot", "advanced", "lightning", "2fa"], "link":"https://electrum.org/"},
			"core": {"tags": ["pc", "windows", "linux", "hot", "node", "full-node", "advanced"], "link":"https://bitcoincore.org/"},
			"knots": {"tags": ["pc", "windows", "linux", "hot", "node", "full-node", "advanced"], "link":"https://bitcoinknots.org/"},
			"wasabi": {"tags": ["pc", "windows", "hot", "privacy"], "link":"https://wasabiwallet.io/"},
			"coldcard": {"tags": ["hardware", "cold", "requires-wallet"], "link":"https://coldcardwallet.com/"},
			"green": {"tags": ["android", "ios", "2fa", "pc", "windows", "linux", "mac", "hot", "node"], "link":"https://blockstream.com/green/"},
			"phoenix": {"tags": ["android", "hot", "lightning", "lightning-node", "easy"], "link":"https://phoenix.acinq.co/"},
			"lnd": {"tags": ["pc", "windows", "linux", "mac", "hot", "node", "lightning", "lightning-node", "advanced"], "link":"https://github.com/lightningnetwork/lnd/releases"}
			}
		resp = "\n"
		for wallet in walletDic:
			if args[0][0].lower() == wallet:
				await ctx.channel.send(wallet[0].upper() + wallet[1:len(wallet)] + ": " + walletDic[wallet]["link"] + " tags: " + ", ".join(walletDic[wallet]["tags"]))
				return
			overlap = list(set(walletDic[wallet]["tags"]) & set(args[0]))
			if len(overlap) > 0:
				resp += wallet[0].upper() + wallet[1:len(wallet)] + ": " + walletDic[wallet]["link"] + " tags: " + ", ".join(walletDic[wallet]["tags"]) + "\n"

		await ctx.channel.send(resp)

	@commands.command()
	async def wallet(self, ctx, *args):
		await Utilities(self).wallets(self, ctx, args)

	@commands.command()
	async def w(self, ctx, *args):
		await Utilities(self).wallets(self, ctx, args)

def setup(bot):
	bot.add_cog(Utilities(bot))