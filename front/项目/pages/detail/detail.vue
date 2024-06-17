<template>
	<view class="content">
		<view class="up">
			<view class="ding">
				<view class="left" @click="block">
					{{$t('detailReturn')}}
				</view>
				<view class="right" @click="toggleLang">
					{{ $t('changeLang') }}
				</view>
			</view>
			<h3 class="titles" style="margin: 0 0 10px;">{{ $t('detailResults') }}</h3>
			<image class="img" :src="imgsrc" v-if="imgsrc" mode=""></image>

			<h3 class="title">{{ detailtitle }}</h3>
			<view class="text">
				{{ detailtext }}
			</view>
		</view>
	</view>

</template>

<script>
	import CryptoJS from 'crypto-js';
	const appId = '20240521002057424';
	const securityKey = '76pOTPXPtU2mcCWDznOT';
	const salt = Math.random().toString(36).slice(-6); // 生成随机数作为salt

	export default {
		data() {
			return {
				imgsrc: '',
				qiehuantext: 'EN',
				detailtitle: '',
				detailtext: '',
				title: ''
			}
		},
		onLoad(data) {
			if (data.img) {
				this.imgsrc = data.img
				this.title = data.title
				this.getdetailtitle()
				this.gpt()
			}
		},
		methods: {
			gpt() {
				uni.hideLoading();
				//显示加载框
				uni.showLoading({
					title: this.$t('Loading')
				});

				uni.request({
					url: 'http://127.0.0.1:5000/gpt-chat',
					method: 'GET',
					data: {
						data: this.title + this.$t('cuoshi')
					},
					success: res => {
						//隐藏加载框
						uni.hideLoading();
						this.detailtext = res.data.message
					},
				})

				// this.detailtext = this.$t('detailtext') //模拟ai返回的数据
			},
			gptzh() {
				if (this.detailtext) {
					let title = this.detailtext
					let from, to;
					if (this.$i18n.locale !== 'en') {
						from = 'en'
						to = 'zh'
					} else {
						from = 'zh'
						to = 'en'
					}
					this.translateText(title, from, to).then(res => {
						if (res.statusCode === 200) {
							this.detailtext = res.data.trans_result[0].dst;
						} else {
							console.error('请求失败，状态码:', res.statusCode);
						}
					})

				}
			},
			getdetailtitle() {
				let title = this.title
				let from, to;
				if (this.$i18n.locale !== 'en') {
					from = 'en'
					to = 'zh'
				} else {
					from = 'zh'
					to = 'en'
				}
				this.translateText(title, from, to).then(res => {
					if (res.statusCode === 200) {
						this.detailtitle = res.data.trans_result[0].dst;
					} else {
						console.error('请求失败，状态码:', res.statusCode);
					}
				})

			},

			toggleLang() {
				this.$i18n.locale = this.$i18n.locale === 'en' ? 'zh' : 'en';
				this.getdetailtitle()
				this.gpt()
			},
			block() {
				uni.hideLoading();
				uni.redirectTo({
					url: '/pages/index/index'
				})
			},
			//翻译接口
			translateText(text, from, to) {
				const sign = CryptoJS.MD5(appId + text + salt + securityKey).toString(); // 使用md5生成签名，注意引入md5库
				const url =
					`https://fanyi-api.baidu.com/api/trans/vip/translate?q=${encodeURIComponent(text)}&from=${from}&to=${to}&appid=${appId}&salt=${salt}&sign=${sign}`;

				let res = uni.request({
					url,
					method: 'GET',
				});
				return res
			},
		}
	}
</script>

<style scoped lang="scss">
	.content {
		width: 100%;
		min-height: 100vh;
		background: url(@/static/1.jpg) no-repeat;
		background-size: cover;
		padding: 4vh 0;
		box-sizing: border-box
			/*是IE盒子模型*/

	}

	.up {
		width: 90%;
		margin: 0 auto;
		border-radius: 20px;
		padding: 50px 0 30px;
		background-color: rgba(255, 255, 255, 0.68);
		text-align: center;
		position: relative;

		.ding {
			position: absolute;
			top: 12px;
			right: 14px;
			display: flex;
			font-size: 1.2em;
			color: #000;
			font-weight: 540;

			.left {
				margin-right: 20px;

			}

			.left:hover {
				color: #007aff;
			}

			.right:hover {
				color: #007aff;
			}
		}

		.img {
			width: 240px;
			// flex: 1;
			border-radius: 8px;
			object-fit: cover;
		}

		.title {
			margin-top: 10px;
			font-size: 1.4em;
		}

		.text {
			width: 90%;
			margin: 10px auto 0;
			text-align: justify;
			font-size: 1em;
			line-height: 1.5em;
			text-indent: 2em;
		}
	}

	.example-body {
		padding: 10px;
		padding-top: 0;
	}

	.custom-image-box {
		/* #ifndef APP-NVUE */
		display: flex;
		/* #endif */
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
	}

	.xt {
		width: 50px;
		height: 50px;
		object-fit: cover;
		margin-right: 10px;
	}

	.topimg {
		width: 90%;
		margin: 0 auto;
		display: flex;

	}

	.text {
		font-size: 14px;
		color: #333;
	}

	::v-deep .uni-file-picker__container {
		justify-content: center;
	}

	::v-deep .file-picker__box {
		width: 200px !important;
		height: 200px !important;
	}

	::v-deep .uni-progress-bar {
		background: none !important;
	}

	.button {
		width: 70%;
		margin-top: 20px;
	}
</style>