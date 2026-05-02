const fs = require('fs');
const path = require('path');

const dataDir = '/Users/gejiayu/owner/seo/data/scooter-moped-rental-tools';

// Proper Chinese titles for each file
const titleMap = {
  'electric-scooter-insurance-management-systems-insuretech-vs-scootinsure-vs-fleetguard-2026-zh.json': '电动滑板车保险管理系统2026年：InsureTech vs ScootInsure vs FleetGuard五大保险平台对比',
  'electric-scooter-maintenance-management-system-guide-zh.json': '电动滑板车维护管理系统指南：保养追踪与故障诊断工具2026年',
  'electric-scooter-maintenance-management-systems-fleetminder-vs-scootfix-vs-maintenancepro-2026-zh.json': '电动滑板车维护管理系统2026年：FleetMinder vs ScootFix vs MaintenancePro五大维护平台对比',
  'electric-scooter-mobile-app-management-system-guide-zh.json': '电动滑板车移动应用管理系统指南：App运营与用户体验工具2026年',
  'electric-scooter-payment-processing-systems-stripe-vs-square-vs-adyen-2026-zh.json': '电动滑板车支付处理系统2026年：Stripe vs Square vs Adyen五大支付平台对比',
  'electric-scooter-rental-data-analytics-platform-guide-zh.json': '电动滑板车租赁数据分析平台指南：运营洞察与决策支持工具2026年',
  'electric-scooter-rental-management-system-review-zh.json': '电动滑板车租赁管理系统评测：车队运营与客户服务工具2026年',
  'electric-scooter-safety-compliance-systems-safetytech-vs-scootsafe-vs-compliancepro-2026-zh.json': '电动滑板车安全合规系统2026年：SafetyTech vs ScootSafe vs CompliancePro五大合规平台对比',
  'electric-scooter-sustainability-management-system-guide-zh.json': '电动滑板车可持续发展管理系统指南：碳减排与绿色运营工具2026年',
  'motorcycle-rental-booking-management-system-guide-zh.json': '摩托车租赁预订管理系统指南：订单处理与客户门户工具2026年',
  'motorcycle-rental-crm-system-guide-zh.json': '摩托车租赁CRM系统指南：客户管理与销售跟进工具2026年',
  'motorcycle-rental-payment-management-system-guide-zh.json': '摩托车租赁支付管理系统指南：收款处理与财务对账工具2026年',
  'scooter-rental-customer-experience-management-system-guide-zh.json': '滑板车租赁客户体验管理系统指南：满意度提升与服务优化工具2026年',
  'scooter-rental-financial-management-software-guide-zh.json': '滑板车租赁财务管理软件指南：成本核算与盈利分析工具2026年',
  'scooter-rental-insurance-management-system-guide-zh.json': '滑板车租赁保险管理系统指南：风险评估与理赔处理工具2026年',
  'scooter-rental-safety-compliance-management-system-guide-zh.json': '滑板车租赁安全合规管理系统指南：法规遵守与风险防控工具2026年',
  'scooter-rental-third-party-platform-integration-system-guide-zh.json': '滑板车租赁第三方平台集成系统指南：API对接与数据同步工具2026年'
};

const descMap = {
  'electric-scooter-insurance-management-systems-insuretech-vs-scootinsure-vs-fleetguard-2026-zh.json': '对比电动滑板车租赁五大保险管理系统，评估InsureTech、ScootInsure、FleetGuard平台在风险评估、理赔处理、合规管理方面的能力。了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！',
  'electric-scooter-maintenance-management-system-guide-zh.json': '电动滑板车维护管理系统完全指南，详解保养追踪、故障诊断、预防性维护等核心功能。了解系统选型要点，找到最适合你的维护方案！专业评测助你决策！',
  'electric-scooter-maintenance-management-systems-fleetminder-vs-scootfix-vs-maintenancepro-2026-zh.json': '对比电动滑板车五大维护管理系统，评估FleetMinder、ScootFix、MaintenancePro平台在保养追踪、故障诊断方面的能力。了解更多功能和价格对比，找到最适合你的方案！专业评测助你决策！',
  'electric-scooter-mobile-app-management-system-guide-zh.json': '电动滑板车移动应用管理系统完全指南，详解App运营、用户体验优化、推送通知等核心功能。了解系统选型要点，找到最适合你的移动方案！专业评测助你决策！',
  'electric-scooter-payment-processing-systems-stripe-vs-square-vs-adyen-2026-zh.json': '对比电动滑板车五大支付处理系统，评估Stripe、Square、Adyen平台在支付安全、交易处理方面的能力。了解更多功能和价格对比，找到最适合你的支付方案！专业评测助你决策！',
  'electric-scooter-rental-data-analytics-platform-guide-zh.json': '电动滑板车租赁数据分析平台完全指南，详解运营洞察、决策支持、预测分析等核心功能。了解平台选型要点，找到最适合你的数据分析方案！专业评测助你决策！',
  'electric-scooter-rental-management-system-review-zh.json': '电动滑板车租赁管理系统深度评测，涵盖车队运营、客户服务、订单管理等核心功能。了解系统功能与价格对比，找到最适合你的租赁方案！专业评测助你决策！',
  'electric-scooter-safety-compliance-systems-safetytech-vs-scootsafe-vs-compliancepro-2026-zh.json': '对比电动滑板车五大安全合规系统，评估SafetyTech、ScootSafe、CompliancePro平台在法规遵守、风险防控方面的能力。了解更多功能和价格对比，找到最适合你的合规方案！专业评测助你决策！',
  'electric-scooter-sustainability-management-system-guide-zh.json': '电动滑板车可持续发展管理系统完全指南，详解碳减排、绿色运营、环保合规等核心功能。了解系统选型要点，找到最适合你的可持续发展方案！专业评测助你决策！',
  'motorcycle-rental-booking-management-system-guide-zh.json': '摩托车租赁预订管理系统完全指南，详解订单处理、客户门户、电子合同等核心功能。了解系统选型要点，找到最适合你的预订方案！专业评测助你决策！',
  'motorcycle-rental-crm-system-guide-zh.json': '摩托车租赁CRM系统完全指南，详解客户管理、销售跟进、客户分析等核心功能。了解系统选型要点，找到最适合你的CRM方案！专业评测助你决策！',
  'motorcycle-rental-payment-management-system-guide-zh.json': '摩托车租赁支付管理系统完全指南，详解收款处理、财务对账、付款追踪等核心功能。了解系统选型要点，找到最适合你的支付方案！专业评测助你决策！',
  'scooter-rental-customer-experience-management-system-guide-zh.json': '滑板车租赁客户体验管理系统完全指南，详解满意度提升、服务优化、反馈收集等核心功能。了解系统选型要点，找到最适合你的客户体验方案！专业评测助你决策！',
  'scooter-rental-financial-management-software-guide-zh.json': '滑板车租赁财务管理软件完全指南，详解成本核算、盈利分析、财务报表等核心功能。了解软件选型要点，找到最适合你的财务方案！专业评测助你决策！',
  'scooter-rental-insurance-management-system-guide-zh.json': '滑板车租赁保险管理系统完全指南，详解风险评估、理赔处理、保险合规等核心功能。了解系统选型要点，找到最适合你的保险方案！专业评测助你决策！',
  'scooter-rental-safety-compliance-management-system-guide-zh.json': '滑板车租赁安全合规管理系统完全指南，详解法规遵守、风险防控、安全检查等核心功能。了解系统选型要点，找到最适合你的合规方案！专业评测助你决策！',
  'scooter-rental-third-party-platform-integration-system-guide-zh.json': '滑板车租赁第三方平台集成系统完全指南，详解API对接、数据同步、平台整合等核心功能。了解系统选型要点，找到最适合你的集成方案！专业评测助你决策！'
};

let fixed = 0;
Object.keys(titleMap).forEach(file => {
  const filePath = path.join(dataDir, file);
  if (fs.existsSync(filePath)) {
    try {
      const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
      data.title = titleMap[file];
      data.description = descMap[file];
      data.author = '电动滑板车运营专家';
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
      fixed++;
    } catch (err) {
      console.log('Error:', file, err.message);
    }
  }
});
console.log('Fixed:', fixed, 'files');
