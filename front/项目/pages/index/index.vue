<template>
	<view class="content">
		<view class="up">
			<view class="ding">
				<view class="right" @click="toggleLang">
					{{ $t('changeLang') }}
				</view>
			</view>
			<h3 class="title">{{ $t('indextitle') }}</h3>
			<uni-section title="" type="line">
				<view class="example-body">
					<uni-file-picker :limit="1" @select="select">
						<view class="custom-plus-button">
							<text>{{ $t('indexupdata') }}</text>
						</view>
					</uni-file-picker>
				</view>
			</uni-section>
			<button class="button" type="primary" @click="submit">{{ $t('indexsubmit') }}</button>
		</view>
		<uni-popup ref="message" type="message">
			<uni-popup-message type="error" :message="$t('indexmessage')" :duration="2000"></uni-popup-message>
		</uni-popup>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				fileLists: '',
			}
		},
		onLoad() {

		},
		methods: {
			toggleLang() {
				this.$i18n.locale = this.$i18n.locale === 'en' ? 'zh' : 'en';
			},
			submit() {
				let title = this.$t('detailtitle')
				// 跳转分页
				uni.redirectTo({
					url: `../detail/detail?img=${this.fileLists.tempFilePaths[0]}&title=${title}`
				})

				// if (this.fileLists.tempFilePaths) {
				// 	this.fileLists.tempFiles[0].file.url = this.fileLists.tempFiles[0].file.path
				// 	//console.log(this.fileLists.tempFiles[0].file);
				// 	uni.uploadFile({
				// 		url: 'http://127.0.0.1:5000/upload',
				// 		file: this.fileLists.tempFiles[0].file,
				// 		filePath: this.fileLists.tempFiles[0].file.path, // 
				// 		// 文件

				// 		// uni.request({
				// 		//       url: 'http://127.0.0.1:5000/upload',
				// 		//       data: {
				// 		//        file: this.fileLists.tempFilePaths[0]
				// 		//       }, // 文件
				// 		//       method: 'POST',
				// 		name: 'file', // 在FormData 中文件对应的属性名
				// 		success: res => {
				// 			console.log(res);
				// 			//let title = res.data.predicted_text?res.data.predicted_text:this.$t('detailtitle') //模拟数据
				// 			let title = JSON.parse(res.data).predicted_text
				// 			console.log(title, 111);
				// 			// 跳转分页
				// 			uni.redirectTo({
				// 				url: `../detail/detail?img=${this.fileLists.tempFilePaths[0]}&title=${title}`
				// 			})
				// 		},
				// 		fail: res => {

				// 			console.log(res, 'err');
				// 		}
				// 	})


				// } else {
				// 	this.$refs.message.open()
				// }

			},
			// 获取上传状态
			select(e) {
				this.fileLists = e
			},

		}
	}
</script>

<style scoped lang="scss">
	.content {
		width: 100%;
		height: 100vh;
		background: url(@/static/1.jpg) no-repeat;
		background-size: cover;
		padding-top: 20vh;
		box-sizing: border-box
			/*是IE盒子模型*/

	}

	.title {
		text-align: center;
		margin-bottom: 10px;
	}

	.up {
		width: 90%;
		margin: 0 auto;
		border-radius: 20px;
		padding: 30px 0;
		background-color: rgba(255, 255, 255, 0.5);
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
		margin-top: 10px;
	}

	.custom-plus-button {
		padding: 0 10px;
	}
</style>