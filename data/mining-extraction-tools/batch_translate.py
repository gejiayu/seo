#!/usr/bin/env python3
"""
Batch translate Chinese JSON files to American English.
Processes title, description, content, seo_keywords fields.
Adds "language": "en-US" field.
"""

import json
import re
from pathlib import Path
from typing import Dict, List

DATA_DIR = Path("/Users/gejiayu/owner/seo/data/mining-extraction-tools")
CHINESE_PATTERN = re.compile(r'[一-鿿]')

# Translation mappings for common mining terms
MINING_TERMS = {
    "矿山": "Mine",
    "开采": "Mining",
    "管理": "Management",
    "系统": "System",
    "智能化": "Intelligent",
    "自动化": "Automation",
    "监测": "Monitoring",
    "预警": "Warning/Alert",
    "调度": "Dispatch/Scheduling",
    "设备": "Equipment",
    "安全": "Safety",
    "生产": "Production",
    "运营": "Operations",
    "数据": "Data",
    "分析": "Analysis",
    "优化": "Optimization",
    "无人驾驶": "Autonomous/Driverless",
    "远程操控": "Remote Control",
    "井下": "Underground",
    "瓦斯": "Gas",
    "煤矿": "Coal Mine",
    "铁矿": "Iron Mine",
    "铜矿": "Copper Mine",
    "金矿": "Gold Mine",
    "锂矿": "Lithium Mine",
    "智能化矿山": "Intelligent Mine",
    "数字化": "Digital",
    "智能化转型": "Intelligent Transformation",
    "全流程": "Full-Process",
    "核心工具": "Core Tools",
    "评测": "Review",
    "深度分析": "Deep Analysis",
    "行业背景": "Industry Background",
    "市场驱动": "Market Drivers",
    "功能模块": "Function Modules",
    "深度评测": "Deep Review",
    "功能对比": "Feature Comparison",
    "选型决策": "Selection Decision",
    "发展趋势": "Development Trends",
    "结论与建议": "Conclusions and Recommendations",
    "产品概述": "Product Overview",
    "核心优势": "Core Advantages",
    "技术架构": "Technical Architecture",
    "实施案例": "Implementation Case",
    "适用对象": "Applicable Targets",
    "价格范围": "Price Range",
    "性价比": "Value/Cost-Effective",
    "标杆": "Benchmark/Standard",
    "新兴": "Emerging",
    "创新": "Innovative",
    "方案": "Solution",
    "完整方案": "Complete Solution",
    "基础方案": "Basic Solution",
    "预算有限": "Budget-Constrained",
    "大型": "Large-Scale",
    "中型": "Medium-Scale",
    "跨国": "Transnational/International",
    "偏远地区": "Remote Areas",
    "现场": "On-Site",
    "效率提升": "Efficiency Improvement",
    "成本降低": "Cost Reduction",
    "安全水平": "Safety Level",
    "关键窗口期": "Critical Window Period",
    "成熟度": "Maturity",
    "转折点": "Turning Point",
    "路线图": "Roadmap",
    "分阶段": "Phased",
    "部署": "Deployment",
    "普及率": "Adoption Rate",
    "渗透率": "Penetration Rate",
    "行业标准": "Industry Standard",
    "基准": "Benchmark",
    "优秀": "Excellent",
    "良好": "Good",
    "中等": "Medium",
    "基础": "Basic",
    "完整": "Complete",
    "精简实用": "Streamlined and Practical",
    "AI驱动": "AI-Driven",
    "AI原生": "AI-Native",
    "深度学习": "Deep Learning",
    "算法": "Algorithm",
    "预测": "Prediction",
    "智能": "Smart/Intelligent",
    "全功能": "Full-Function",
    "核心功能": "Core Functions",
    "辅助功能": "Auxiliary Functions",
    "关键功能": "Key Functions",
    "必备功能": "Essential Functions",
    "附加值": "Value-Added",
    "竞争力": "Competitiveness",
    "市场份额": "Market Share",
    "应用最广泛": "Most Widely Applied",
    "领先": "Leading",
    "创新功能": "Innovative Features",
    "特色": "Features/Characteristics",
    "亮点": "Highlights",
    "优势": "Advantages",
    "强项": "Strengths",
    "弱项": "Weaknesses",
    "不足": "Limitations",
    "挑战": "Challenges",
    "机遇": "Opportunities",
    "风险": "Risks",
    "收益": "Benefits/Returns",
    "回报": "Return",
    "投资": "Investment",
    "成本": "Cost",
    "费用": "Expense",
    "许可证": "License",
    "订阅": "Subscription",
    "SaaS": "SaaS",
    "云端": "Cloud",
    "本地部署": "On-Premise Deployment",
    "移动端": "Mobile",
    "原生应用": "Native Application",
    "API": "API",
    "集成": "Integration",
    "对接": "Connection/Integration",
    "兼容": "Compatible",
    "支持": "Support",
    "免费试用": "Free Trial",
    "试用期": "Trial Period",
    "年费": "Annual Fee",
    "月费": "Monthly Fee",
    "实施周期": "Implementation Period",
    "总投资": "Total Investment",
    "维护费": "Maintenance Fee",
    "额外收费": "Additional Charge",
    "按等级计费": "Tiered Pricing",
    "无费用": "No Fee",
    "年维护费": "Annual Maintenance Fee",
    "性价比高": "High Value",
    "预算约束": "Budget Constraints",
    "预算分配": "Budget Allocation",
    "技术接受度": "Technology Acceptance",
    "创新型企业": "Innovative Enterprises",
    "保守型企业": "Conservative Enterprises",
    "传统": "Traditional",
    "成熟稳定": "Mature and Stable",
    "试点": "Pilot",
    "全面建设": "Full-Scale Construction",
    "普及": "Popularization",
    "应用": "Application",
    "推广": "Promotion",
    "落地": "Implementation",
    "实操": "Practical Operation",
    "实战": "Real-World",
    "案例": "Case",
    "典型案例": "Typical Case",
    "成功案例": "Success Case",
    "标杆案例": "Benchmark Case",
    "用户": "User",
    "客户": "Customer",
    "企业": "Enterprise",
    "公司": "Company",
    "组织": "Organization",
    "团队": "Team",
    "部门": "Department",
    "角色": "Role",
    "职责": "Responsibility",
    "权限": "Permission",
    "账号": "Account",
    "登录": "Login",
    "认证": "Authentication",
    "授权": "Authorization",
    "安全合规": "Security Compliance",
    "法规": "Regulation",
    "标准": "Standard",
    "规范": "Specification",
    "规程": "Protocol",
    "法案": "Act",
    "政策": "Policy",
    "强制": "Mandatory",
    "鼓励": "Encourage",
    "推动": "Promote",
    "升级": "Upgrade",
    "转型": "Transformation",
    "改革": "Reform",
    "创新": "Innovation",
    "突破": "Breakthrough",
    "进展": "Progress",
    "成就": "Achievement",
    "效果": "Effect",
    "成果": "Result",
    "业绩": "Performance",
    "指标": "Indicator",
    "准确率": "Accuracy Rate",
    "效率": "Efficiency",
    "性能": "Performance",
    "稳定性": "Stability",
    "可靠性": "Reliability",
    "可用性": "Availability",
    "扩展性": "Scalability",
    "兼容性": "Compatibility",
    "灵活性": "Flexibility",
    "易用性": "Usability",
    "可维护性": "Maintainability",
    "安全性": "Security",
    "隐私": "Privacy",
    "保护": "Protection",
    "防护": "Defense",
    "应急": "Emergency",
    "响应": "Response",
    "处理": "Handling",
    "解决": "Solution",
    "应对": "Response",
    "预防": "Prevention",
    "避免": "Avoidance",
    "减少": "Reduction",
    "消除": "Elimination",
    "控制": "Control",
    "管理": "Management",
    "治理": "Governance",
    "监督": "Supervision",
    "检查": "Inspection",
    "测试": "Testing",
    "验证": "Verification",
    "确认": "Confirmation",
    "审批": "Approval",
    "签字": "Signature",
    "备案": "Record",
    "归档": "Archive",
    "存储": "Storage",
    "备份": "Backup",
    "恢复": "Recovery",
    "迁移": "Migration",
    "转换": "Conversion",
    "格式": "Format",
    "结构": "Structure",
    "组织": "Organization",
    "分类": "Classification",
    "标签": "Tag",
    "索引": "Index",
    "查询": "Query",
    "检索": "Search",
    "过滤": "Filter",
    "排序": "Sort",
    "分组": "Group",
    "聚合": "Aggregation",
    "统计": "Statistics",
    "报表": "Report",
    "图表": "Chart",
    "可视化": "Visualization",
    "仪表盘": "Dashboard",
    "展示": "Display",
    "呈现": "Presentation",
    "输出": "Output",
    "输入": "Input",
    "导入": "Import",
    "导出": "Export",
    "打印": "Print",
    "下载": "Download",
    "上传": "Upload",
    "分享": "Share",
    "协作": "Collaboration",
    "沟通": "Communication",
    "通知": "Notification",
    "提醒": "Reminder",
    "消息": "Message",
    "邮件": "Email",
    "短信": "SMS",
    "即时通讯": "Instant Messaging",
    "在线": "Online",
    "实时": "Real-Time",
    "历史": "History",
    "记录": "Record",
    "日志": "Log",
    "追踪": "Tracking",
    "溯源": "Tracing",
    "定位": "Positioning",
    "导航": "Navigation",
    "地图": "Map",
    "地理": "Geographic",
    "空间": "Spatial",
    "三维": "3D",
    "模型": "Model",
    "建模": "Modeling",
    "仿真": "Simulation",
    "虚拟": "Virtual",
    "现实": "Reality",
    "增强现实": "Augmented Reality",
    "虚拟现实": "Virtual Reality",
    "混合现实": "Mixed Reality",
    "数字孪生": "Digital Twin",
    "镜像": "Mirror",
    "映射": "Mapping",
    "对应": "Correspondence",
    "关联": "Association",
    "关系": "Relationship",
    "连接": "Connection",
    "链接": "Link",
    "绑定": "Binding",
    "同步": "Synchronization",
    "异步": "Asynchronous",
    "并发": "Concurrency",
    "并行": "Parallel",
    "串行": "Serial",
    "顺序": "Sequential",
    "流程": "Process",
    "环节": "Stage",
    "步骤": "Step",
    "任务": "Task",
    "作业": "Job",
    "工作": "Work",
    "活动": "Activity",
    "事件": "Event",
    "操作": "Operation",
    "执行": "Execution",
    "完成": "Completion",
    "进度": "Progress",
    "状态": "Status",
    "结果": "Result",
    "产出": "Output",
    "交付": "Delivery",
    "验收": "Acceptance",
    "质量": "Quality",
    "数量": "Quantity",
    "规格": "Specification",
    "参数": "Parameter",
    "配置": "Configuration",
    "设置": "Setting",
    "选项": "Option",
    "属性": "Attribute",
    "特征": "Feature",
    "标签": "Label",
    "标记": "Mark",
    "符号": "Symbol",
    "图标": "Icon",
    "图示": "Illustration",
    "示例": "Example",
    "样例": "Sample",
    "模板": "Template",
    "样式": "Style",
    "布局": "Layout",
    "设计": "Design",
    "架构": "Architecture",
    "框架": "Framework",
    "平台": "Platform",
    "引擎": "Engine",
    "工具": "Tool",
    "组件": "Component",
    "模块": "Module",
    "插件": "Plugin",
    "扩展": "Extension",
    "应用": "Application",
    "软件": "Software",
    "硬件": "Hardware",
    "设备": "Device",
    "终端": "Terminal",
    "传感器": "Sensor",
    "控制器": "Controller",
    "执行器": "Actuator",
    "驱动": "Driver",
    "接口": "Interface",
    "端口": "Port",
    "协议": "Protocol",
    "网络": "Network",
    "通信": "Communication",
    "传输": "Transmission",
    "连接": "Connection",
    "链路": "Link",
    "通道": "Channel",
    "路径": "Path",
    "路由": "Route",
    "网关": "Gateway",
    "代理": "Proxy",
    "服务器": "Server",
    "客户端": "Client",
    "主机": "Host",
    "节点": "Node",
    "集群": "Cluster",
    "分布式": "Distributed",
    "集中式": "Centralized",
    "混合式": "Hybrid",
    "边缘计算": "Edge Computing",
    "云计算": "Cloud Computing",
    "物联网": "IoT",
    "互联网": "Internet",
    "内网": "Intranet",
    "外网": "Extranet",
    "专网": "Private Network",
    "公网": "Public Network",
    "局域网": "LAN",
    "广域网": "WAN",
    "城域网": "MAN",
    "无线": "Wireless",
    "有线": "Wired",
    "蓝牙": "Bluetooth",
    "WiFi": "WiFi",
    "5G": "5G",
    "4G": "4G",
    "LTE": "LTE",
    "NB-IoT": "NB-IoT",
    "LoRa": "LoRa",
    "ZigBee": "ZigBee",
    "射频": "RF",
    "红外": "Infrared",
    "超声波": "Ultrasound",
    "激光": "Laser",
    "雷达": "Radar",
    "GPS": "GPS",
    "北斗": "BeiDou",
    "GLONASS": "GLONASS",
    "伽利略": "Galileo",
    "定位系统": "Positioning System",
    "导航系统": "Navigation System",
    "GIS": "GIS",
    "地图服务": "Map Service",
    "地理信息": "Geographic Information",
    "空间数据": "Spatial Data",
    "遥感": "Remote Sensing",
    "卫星": "Satellite",
    "航空": "Aerial",
    "无人机": "UAV/Drone",
    "机器人": "Robot",
    "机械臂": "Robotic Arm",
    "自动驾驶": "Autonomous Driving",
    "智能驾驶": "Intelligent Driving",
    "辅助驾驶": "Assisted Driving",
    "无人驾驶": "Driverless",
    "远程驾驶": "Remote Driving",
    "操控": "Control",
    "控制": "Control",
    "调节": "Adjustment",
    "优化": "Optimization",
    "决策": "Decision",
    "规划": "Planning",
    "设计": "Design",
    "评估": "Evaluation",
    "测试": "Testing",
    "验证": "Verification",
    "确认": "Validation",
    "实施": "Implementation",
    "运维": "Operations & Maintenance",
    "维护": "Maintenance",
    "检修": "Repair",
    "保养": "Maintenance",
    "更换": "Replacement",
    "升级": "Upgrade",
    "迭代": "Iteration",
    "版本": "Version",
    "更新": "Update",
    "发布": "Release",
    "部署": "Deployment",
    "安装": "Installation",
    "配置": "Configuration",
    "调试": "Debugging",
    "优化": "Optimization",
    "调优": "Tuning",
    "性能优化": "Performance Optimization",
    "资源优化": "Resource Optimization",
    "流程优化": "Process Optimization",
    "调度优化": "Scheduling Optimization",
    "路径优化": "Path Optimization",
    "成本优化": "Cost Optimization",
    "效率优化": "Efficiency Optimization",
    "质量优化": "Quality Optimization",
    "安全优化": "Safety Optimization",
    "环境优化": "Environment Optimization",
}

def has_chinese(text: str) -> bool:
    """Check if text contains Chinese characters."""
    if not text:
        return False
    return bool(CHINESE_PATTERN.search(text))

def translate_chinese_to_english(text: str) -> str:
    """
    Translate Chinese text to natural American English.
    Uses semantic understanding and mining domain terminology.
    """
    if not text or not has_chinese(text):
        return text

    # This is a placeholder - actual translation will be done by AI
    # In production, this would call an AI translation service
    # For now, return the text as-is to be processed manually
    return text

def process_file(file_path: Path) -> bool:
    """
    Process a single JSON file and translate Chinese content.
    Returns True if file was modified, False otherwise.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check if file needs translation
        if not has_chinese(str(data.get('title', ''))) and \
           not has_chinese(str(data.get('description', ''))) and \
           not has_chinese(str(data.get('content', ''))):
            # File already in English, just add language field if missing
            if 'language' not in data:
                data['language'] = 'en-US'
                # Ensure seo_keywords is array
                if not isinstance(data.get('seo_keywords', []), list):
                    if isinstance(data.get('seo_keywords'), str):
                        data['seo_keywords'] = [data['seo_keywords']]
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True
            return False

        # File has Chinese content - needs translation
        print(f"\nTranslating: {file_path.name}")

        # Translate title
        if has_chinese(data.get('title', '')):
            original_title = data['title']
            print(f"  Original title: {original_title}")
            # Translation will be done manually via AI

        # Translate description
        if has_chinese(data.get('description', '')):
            original_desc = data['description']
            print(f"  Original description: {original_desc[:100]}...")

        # Translate content
        if has_chinese(data.get('content', '')):
            print(f"  Content contains Chinese (length: {len(data['content'])} chars)")

        # Translate seo_keywords
        keywords = data.get('seo_keywords', [])
        if isinstance(keywords, list):
            chinese_keywords = [kw for kw in keywords if has_chinese(str(kw))]
            if chinese_keywords:
                print(f"  Chinese keywords: {chinese_keywords}")

        return True

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    print("=" * 80)
    print("Mining-Extraction-Tools Chinese File Translation")
    print("=" * 80)

    # Find all files with Chinese content
    chinese_files = []
    for json_file in DATA_DIR.glob("*.json"):
        if json_file.name.startswith("detect_") or json_file.name == "chinese_files_list.txt":
            continue
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if has_chinese(str(data.get('title', ''))) or \
                   has_chinese(str(data.get('description', ''))) or \
                   has_chinese(str(data.get('content', ''))):
                    chinese_files.append(json_file)
        except Exception as e:
            print(f"Error reading {json_file}: {e}")

    print(f"\nFound {len(chinese_files)} files with Chinese content")

    # Process each file
    modified_count = 0
    for i, file_path in enumerate(chinese_files, 1):
        print(f"\n[{i}/{len(chinese_files)}] Processing: {file_path.name}")
        if process_file(file_path):
            modified_count += 1

    print(f"\n" + "=" * 80)
    print(f"Total files processed: {len(chinese_files)}")
    print(f"Files needing translation: {modified_count}")
    print("=" * 80)

if __name__ == "__main__":
    main()