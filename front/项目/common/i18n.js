import {
	createI18n
} from 'vue-i18n';

const messages = {
	en: {
		changeLang: 'EN',
		indextitle: 'Choose your plant',
		indexupdata: 'Click to take a picture or upload',
		indexmessage: 'Please select the picture first',
		indexsubmit: 'submit',
		detailReturn: 'Return',
		detailtitle: 'Apple scab is serious',
		detailtext: 'Apple scab, also known as apple scab, black spot disease, is caused by apple scab infection, occurs on the apple disease. It mainly harms leaves or fruits, petioles, fruit stalks, flower buds, flower organs and new shoots, from falling flower stage to apple ripening stage. The prevention and control of apple scab should be based on the principle of prevention and treatment in order to effectively control the occurrence of the disease and reduce the harm. Disease-resistant varieties were selected in orchards with serious disease. After autumn, clean the orchard, collect fallen leaves, burn or bury them deeply, or use 5% urea to accelerate the decomposition of fallen leaves by microorganisms. Fruit trees in dense planting orchards and old orchards should be thinned, irrigated at the right time, and applied more organic fertilizer, phosphorus and potassium fertilizer. Popularize and apply bagging technology.',
		detailResults: 'Results',
	},
	zh: {
		changeLang: 'ZH',
		indextitle: '选择你的植物',
		indexupdata: '点击拍照或上传',
		indexmessage: '请先选择图片',
		indexsubmit: '提交',
		detailReturn: '返回',
		detailtitle: '苹果黑星病严重',
		detailtext: '苹果黑星病又称苹果疮痂病、黑点病，是由苹果黑星菌侵染所引起的、发生在苹果上的病害。主要危害叶片或果实，叶柄、果柄、花芽、花器及新梢，从落花期到苹果成熟期均可危害。苹果黑星病防治时应坚持预防为主，治疗为辅的原则，以有效地控制病害的发生，减轻危害。发病严重的果园选栽抗病品种。秋后清扫果园，收集落叶，烧毁或深埋，或用5%尿素处理加速微生物对落叶的分解。果树密植园和老果园要进行疏树，适时灌水，增施有机肥、磷钾肥。推广应用套袋技术。',
		detailResults: '结果',
	},
};

const i18n = createI18n({
	locale: 'en', // 设置默认语言
	messages,
});

export default i18n;