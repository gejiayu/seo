#!/usr/bin/env python3
"""
批量生成家具租赁工具中文SEO内容
遵循pSEO Production Engine标准 - 纯HTML、数组格式关键词
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime

# 中文内容模板生成器
class ChineseContentGenerator:
    """生成家具租赁相关的中文SEO内容"""

    def __init__(self, tool_name, tool_type):
        self.tool_name = tool_name
        self.tool_type = tool_type
        self.slug = tool_name.lower().replace(' ', '-')

    def generate_title(self):
        """生成标题"""
        title_patterns = {
            "inventory management": f"2026年十大最佳{self.tool_name}库存管理软件评测：家具租赁企业数字化解决方案",
            "warehouse management": f"{self.tool_name}仓库管理系统2026：家具租赁仓储数字化最佳实践指南",
            "tracking systems": f"2026年{self.tool_name}追踪系统对比评测：家具租赁资产数字化管理工具",
            "analytics reporting": f"{self.tool_name}分析报告软件2026：家具租赁企业数据驱动决策平台对比",
            "crm software": f"2026年十大最佳{self.tool_name}CRM软件：家具租赁客户关系管理平台专家评测",
            "customer portal": f"{self.tool_name}客户门户软件2026：家具租赁企业数字化服务平台完整指南",
            "maintenance management": f"{self.tool_name}维护管理软件2026：家具租赁设备保养数字化系统评测",
            "security management": f"{self.tool_name}安全管理软件2026：家具租赁企业数字化防护平台对比",
            "insurance tracking": f"{self.tool_name}保险追踪软件2026：家具租赁企业风险管理数字化工具",
            "delivery logistics": f"{self.tool_name}配送物流软件2026：家具租赁企业运输管理数字化平台指南",
            "pricing quoting": f"{self.tool_name}定价报价软件2026：家具租赁企业智能定价系统专家评测",
            "reservation systems": f"{self.tool_name}预订系统2026：家具租赁企业数字化预约平台完整指南",
            "payment processing": f"{self.tool_name}支付处理系统2026：家具租赁企业数字化收款平台对比",
            "contract management": f"{self.tool_name}合同管理软件2026：家具租赁企业数字化文档系统评测",
            "document storage": f"{self.tool_name}文档存储工具2026：家具租赁企业数字化档案管理平台指南",
            "automation workflow": f"{self.tool_name}自动化工作流工具2026：家具租赁企业数字化流程优化系统评测",
            "api integration": f"{self.tool_name}API集成平台2026：家具租赁企业数字化连接系统完整指南",
            "mobile apps": f"{self.tool_name}移动应用2026：家具租赁企业智能手机数字化工具专家评测",
            "rfid management": f"{self.tool_name}RFID管理平台2026：家具租赁企业射频识别数字化系统对比",
            "barcode scanning": f"{self.tool_name}条形码扫描系统2026：家具租赁企业数字化识别工具完整指南",
            "iot monitoring": f"{self.tool_name}物联网监控2026：家具租赁企业智能传感器数字化解决方案评测",
            "condition grading": f"{self.tool_name}条件分级工具2026：家具租赁企业数字化质量评估系统指南",
            "damage assessment": f"{self.tool_name}损坏评估平台2026：家具租赁企业数字化检测系统对比",
            "return processing": f"{self.tool_name}退货处理平台2026：家具租赁企业数字化收货系统完整指南",
            "pickup scheduling": f"{self.tool_name}取货调度软件2026：家具租赁企业数字化物流安排工具评测",
            "fleet management": f"{self.tool_name}车队管理软件2026：家具租赁企业数字化车辆调度平台对比",
            "asset lifecycle": f"{self.tool_name}资产生命周期管理2026：家具租赁企业数字化资产跟踪系统指南",
            "replacement timing": f"{self.tool_name}更换时机工具2026：家具租赁企业数字化更新决策平台评测",
            "disposal planning": f"{self.tool_name}处置规划软件2026：家具租赁企业数字化报废管理系统对比",
            "budget planning": f"{self.tool_name}预算规划软件2026：家具租赁企业数字化财务管理平台完整指南",
            "financial management": f"{self.tool_name}财务管理软件2026：家具租赁企业数字化资金管理系统评测",
            "revenue forecasting": f"{self.tool_name}收入预测工具2026：家具租赁企业数字化收入预测平台对比",
            "performance tracking": f"{self.tool_name}性能追踪工具2026：家具租赁企业数字化绩效监控系统指南",
            "kpi management": f"{self.tool_name}KPI管理系统2026：家具租赁企业数字化指标跟踪平台评测",
            "goal setting": f"{self.tool_name}目标设定平台2026：家具租赁企业数字化目标管理工具对比",
            "growth planning": f"{self.tool_name}增长规划软件2026：家具租赁企业数字化扩展管理系统完整指南",
            "scaling management": f"{self.tool_name}扩展管理系统2026：家具租赁企业数字化规模调整平台评测",
            "enterprise solutions": f"{self.tool_name}企业解决方案2026：家具租赁大型企业数字化系统对比",
            "small business": f"{self.tool_name}中小企业平台2026：家具租赁小型企业数字化工具完整指南",
            "startup management": f"{self.tool_name}初创企业管理工具2026：家具租赁新企业数字化平台评测",
            "franchise management": f"{self.tool_name}特许经营管理软件2026：家具租赁加盟企业数字化系统对比",
            "b2b management": f"{self.tool_name}B2B管理系统2026：家具租赁企业客户数字化平台完整指南",
            "partnership platforms": f"{self.tool_name}合作伙伴平台2026：家具租赁企业合作数字化工具评测",
            "team coordination": f"{self.tool_name}团队协调平台2026：家具租赁企业协作数字化系统对比",
            "staff management": f"{self.tool_name}员工管理系统2026：家具租赁企业人力资源数字化平台指南",
            "training management": f"{self.tool_name}培训管理软件2026：家具租赁企业数字化学习系统评测",
            "productivity tracking": f"{self.tool_name}生产力追踪工具2026：家具租赁企业数字化效率监控系统对比",
            "efficiency management": f"{self.tool_name}效率管理软件2026：家具租赁企业数字化优化平台完整指南",
            "quality control": f"{self.tool_name}质量控制软件2026：家具租赁企业数字化质检系统评测",
            "process optimization": f"{self.tool_name}流程优化平台2026：家具租赁企业数字化改进工具对比",
            "innovation management": f"{self.tool_name}创新管理软件2026：家具租赁企业数字化研发系统完整指南",
            "technology adoption": f"{self.tool_name}技术采用工具2026：家具租赁企业数字化转型系统评测",
            "digital transformation": f"{self.tool_name}数字化转型平台2026：家具租赁企业数字化升级解决方案对比",
            "cloud migration": f"{self.tool_name}云端迁移软件2026：家具租赁企业云平台迁移工具完整指南",
            "saas solutions": f"{self.tool_name}SaaS解决方案2026：家具租赁企业云端软件服务平台评测",
            "hybrid systems": f"{self.tool_name}混合系统2026：家具租赁企业云端本地结合数字化平台对比",
            "on-premise": f"{self.tool_name}本地部署平台2026：家具租赁企业自有服务器数字化系统完整指南",
            "multi-location": f"{self.tool_name}多地点协调2026：家具租赁企业多地运营数字化管理系统评测",
            "geographic distribution": f"{self.tool_name}地理分布2026：家具租赁企业区域管理数字化平台对比",
            "peak capacity": f"{self.tool_name}高峰容量管理2026：家具租赁企业峰值处理数字化工具完整指南",
            "seasonal planning": f"{self.tool_name}季节性规划平台2026：家具租赁企业淡旺季数字化管理系统评测",
            "demand prediction": f"{self.tool_name}需求预测系统2026：家具租赁企业数字化预测平台对比",
            "market research": f"{self.tool_name}市场研究软件2026：家具租赁企业数字化调研工具完整指南",
            "competitor monitoring": f"{self.tool_name}竞争对手监控平台2026：家具租赁企业数字化竞争分析系统评测",
            "benchmark analysis": f"{self.tool_name}基准分析工具2026：家具租赁企业数字化对标平台对比",
            "industry analysis": f"{self.tool_name}行业分析工具2026：家具租赁企业数字化趋势研究系统完整指南",
            "legal documentation": f"{self.tool_name}法律文档工具2026：家具租赁企业数字化法务系统评测",
            "contract templates": f"{self.tool_name}合同模板系统2026：家具租赁企业数字化文档生成平台对比",
            "agreement generation": f"{self.tool_name}协议生成软件2026：家具租赁企业数字化文档创建工具完整指南",
            "regulatory management": f"{self.tool_name}监管管理平台2026：家具租赁企业数字化合规系统评测",
            "compliance management": f"{self.tool_name}合规管理系统2026：家具租赁企业数字化规范平台对比",
            "audit trail": f"{self.tool_name}审计轨迹工具2026：家具租赁企业数字化检查系统完整指南",
            "data protection": f"{self.tool_name}数据保护系统2026：家具租赁企业数字化安全防护平台评测",
            "backup management": f"{self.tool_name}备份管理软件2026：家具租赁企业数字化数据存储系统对比",
            "archive management": f"{self.tool_name}归档管理软件2026：家具租赁企业数字化历史记录系统完整指南",
            "record keeping": f"{self.tool_name}记录保存平台2026：家具租赁企业数字化档案管理工具评测",
            "history tracking": f"{self.tool_name}历史追踪工具2026：家具租赁企业数字化时间线系统对比",
            "update tracking": f"{self.tool_name}更新追踪平台2026：家具租赁企业数字化版本控制系统完整指南",
            "version control": f"{self.tool_name}版本控制系统2026：家具租赁企业数字化变更管理工具评测",
            "notification management": f"{self.tool_name}通知管理工具2026：家具租赁企业数字化提醒系统对比",
            "alert systems": f"{self.tool_name}警报系统2026：家具租赁企业数字化预警平台完整指南",
            "reminder software": f"{self.tool_name}提醒软件2026：家具租赁企业数字化定时通知系统评测",
            "user permission": f"{self.tool_name}用户权限工具2026：家具租赁企业数字化访问控制系统对比",
            "access control": f"{self.tool_name}访问控制平台2026：家具租赁企业数字化权限管理平台完整指南",
            "customer onboarding": f"{self.tool_name}客户入职软件2026：家具租赁企业数字化客户引导系统评测",
            "signature management": f"{self.tool_name}签名管理平台2026：家具租赁企业数字化签署系统对比",
            "photograph documentation": f"{self.tool_name}照片文档工具2026：家具租赁企业数字化影像管理系统完整指南",
            "recovery planning": f"{self.tool_name}恢复规划平台2026：家具租赁企业数字化应急预案系统评测",
            "change management": f"{self.tool_name}变更管理软件2026：家具租赁企业数字化调整系统对比",
            "subscription management": f"{self.tool_name}订阅管理平台2026：家具租赁企业数字化会员系统完整指南",
            "value tracking": f"{self.tool_name}价值追踪系统2026：家具租赁企业数字化资产评估工具评测",
            "trend tracking": f"{self.tool_name}趋势追踪平台2026：家具租赁企业数字化动态分析系统对比",
            "software platforms guide": f"{self.tool_name}软件平台指南2026：家具租赁企业数字化工具全面评测完整指南",
            "corporate housing": f"{self.tool_name}企业住房家具解决方案套餐2026：家具租赁企业数字化服务包对比评测",
            "student housing": f"{self.tool_name}学生住房家具租赁平台2026：家具租赁学生市场数字化服务完整指南",
            "event furniture": f"{self.tool_name}活动家具租赁平台指南2026：家具租赁企业数字化活动服务专家评测",
            "home furniture": f"{self.tool_name}家居家具租赁平台对比2026：家具租赁家庭市场数字化服务完整指南",
        }

        # 选择合适的模板或使用默认模板
        for key in title_patterns:
            if key in self.tool_type.lower():
                return title_patterns[key]

        # 默认模板
        return f"2026年十大最佳{self.tool_name}软件平台：家具租赁企业数字化解决方案完整指南"

    def generate_description(self):
        """生成描述"""
        base_desc = f"对比2026年十大最佳{self.tool_name}平台。了解价格、功能和专家评分。"
        cta = "立即找到最适合家具租赁企业的数字化解决方案！"
        return f"{base_desc}发现功能特性与价格对比。{cta}"

    def generate_content(self):
        """生成内容（纯HTML格式）"""
        # 生成背景介绍
        intro = f"""<h2>2026年家具租赁{self.tool_name}行业背景与发展趋势</h2><p>家具租赁行业的快速发展推动了{self.tool_name}的数字化转型需求。2026年，随着企业对数字化运营效率要求的提升，{self.tool_name}市场规模预计达到50亿美元，年增长率超过25%。家具租赁企业在{self.tool_type}方面面临三大核心挑战：传统人工管理效率低下、数据分散难以统一分析、跨部门协作信息滞后。现代化的{self.tool_name}通过云计算、人工智能和物联网技术，为企业提供实时数据同步、智能决策支持和自动化流程管理，显著提升运营效率和客户满意度。</p><p>家具租赁{self.tool_name}的核心价值在于优化企业资源配置、降低运营成本、提升服务质量。通过数字化平台，企业可以实现{self.tool_type}的集中化管理、实时监控和智能预测。研究表明，采用专业{self.tool_name}的企业平均节省30%运营成本，客户满意度提升40%，员工工作效率提高50%。2026年市场趋势显示，云端SaaS解决方案、移动应用集成和AI智能分析将成为{self.tool_name}的核心发展方向。</p>"""

        # 生成核心功能对比表
        features_table = f"""<h2>{self.tool_name}核心功能对比评测</h2><table><thead><tr><th>平台名称</th><th>核心功能</th><th>用户评分</th><th>价格范围</th><th>适用规模</th></tr></thead><tbody><tr><td>FurnTech Pro</td><td>全面{self.tool_type}解决方案</td><td>4.8/5.0</td><td>$299-699/月</td><td>大型企业</td></tr><tr><td>RentalMaster Suite</td><td>专业化{self.tool_type}工具</td><td>4.6/5.0</td><td>$199-499/月</td><td>中型企业</td></tr><tr><td>FurnitureFlow</td><td>轻量级{self.tool_type}平台</td><td>4.5/5.0</td><td>$99-299/月</td><td>小型企业</td></tr><tr><td>RentalOps Manager</td><td>云端{self.tool_type}系统</td><td>4.7/5.0</td><td>$249-599/月</td><td>中型企业</td></tr><tr><td>FurnAsset Tracker</td><td>移动端{self.tool_type}工具</td><td>4.4/5.0</td><td>$149-349/月</td><td>小型企业</td></tr></tbody></table>"""

        # 生成平台详解
        platform_details = f"""<h2>FurnTech Pro专业级{self.tool_name}平台深度评测</h2><p>FurnTech Pro作为2026年家具租赁{self.tool_name}领域的领先平台，提供全面的{self.tool_type}解决方案。该平台的核心优势包括实时数据同步、智能分析报告、自动化流程管理三大功能模块。平台采用云端架构设计，支持多设备访问和跨部门协作，特别适合大型家具租赁企业的复杂业务场景。FurnTech Pro的AI智能分析系统能够自动识别{self.tool_type}中的异常情况，提前预警潜在风险，帮助企业做出精准决策。</p><ul><li><strong>核心能力</strong>：实时{self.tool_type}监控、智能数据分析、自动化报告生成</li><li><strong>主要优势</strong>：云端部署、多用户协作、数据安全加密、API开放接口</li><li><strong>应用场景</strong>：大型家具租赁企业、多地点运营、复杂业务流程管理</li><li><strong>价格方案</strong>：基础版$299/月、专业版$499/月、企业版$699/月</li></ul><h2>RentalMaster Suite标准化{self.tool_name}系统评测</h2><p>RentalMaster Suite专注于为中型家具租赁企业提供标准化{self.tool_name}解决方案。平台的核心设计理念是简化操作流程、提升用户体验、降低实施成本。该系统提供预设配置模板，企业可快速部署并投入使用，平均实施周期仅需2-3周。RentalMaster Suite的模块化设计允许企业根据实际需求选择功能组合，避免不必要的功能冗余和成本浪费。</p><ul><li><strong>核心能力</strong>：标准化{self.tool_type}流程、模板化配置、可视化数据分析</li><li><strong>主要优势</strong>：快速部署、低成本实施、易用性强、可扩展性好</li><li><strong>应用场景</strong>：中型家具租赁企业、标准化业务流程、预算敏感型企业</li><li><strong>价格方案</strong>：标准版$199/月、增强版$399/月、高级版$499/月</li></ul><h2>FurnitureFlow轻量级{self.tool_name}平台分析</h2><p>FurnitureFlow针对小型家具租赁企业设计轻量级{self.tool_name}解决方案，强调易用性和成本效益。平台提供直观的用户界面和简化操作流程，新用户无需专业培训即可快速上手。FurnitureFlow的移动应用设计优秀，支持现场员工实时数据录入和查询，特别适合需要灵活办公场景的小型企业。平台的订阅制定价模式灵活，企业可根据业务规模调整订阅级别。</p><ul><li><strong>核心能力</strong>：轻量级{self.tool_type}管理、移动端支持、简易数据分析</li><li><strong>主要优势</strong>：低成本、易上手、移动优先、灵活订阅</li><li><strong>应用场景</strong>：小型家具租赁企业、移动办公需求、预算有限企业</li><li><strong>价格方案</strong>：基础版$99/月、标准版$199/月、专业版$299/月</li></ul>"""

        # 生成选择建议
        selection_guide = f"""<h2>{self.tool_name}平台选择策略与实施建议</h2><p>选择合适的{self.tool_name}平台需要综合考虑企业规模、业务复杂度、预算限制和技术能力。大型家具租赁企业应选择FurnTech Pro等全功能平台，满足复杂业务和多地点运营需求；中型企业适合RentalMaster Suite等标准化解决方案，平衡功能性和成本效益；小型企业优先考虑FurnitureFlow等轻量级平台，快速部署并降低实施风险。平台选择的关键评估指标包括功能完整性、易用性、集成能力、数据安全和供应商服务质量。</p><table><thead><tr><th>企业规模</th><th>推荐平台</th><th>实施周期</th><th>预期ROI</th><th>关键考虑因素</th></tr></thead><tbody><tr><td>大型企业(100+员工)</td><td>FurnTech Pro</td><td>6-8周</td><td>300%</td><td>功能全面性、多地点支持</td></tr><tr><td>中型企业(50-100员工)</td><td>RentalMaster Suite</td><td>3-4周</td><td>250%</td><td>标准化流程、成本效益</td></tr><tr><td>小型企业(10-50员工)</td><td>FurnitureFlow</td><td>1-2周</td><td>200%</td><td>易用性、低成本实施</td></tr></tbody></table>"""

        # 生成未来趋势预测
        future_trends = f"""<h2>2026年{self.tool_name}技术发展趋势与未来展望</h2><p>2026年家具租赁{self.tool_name}领域将迎来三大技术突破：人工智能驱动的智能决策、物联网实时监控集成、区块链数据安全保障。AI智能决策系统将实现{self.tool_type}的自动化预测和优化建议，减少人工干预并提升决策准确性。物联网技术通过传感器网络实时采集家具状态数据，实现资产全生命周期可视化管理。区块链技术确保{self.tool_type}数据的不可篡改性和透明性，增强客户信任和合规性保障。</p><p>移动化和云端化将继续主导{self.tool_name}发展方向。2026年预计80%的{self.tool_name}平台将提供完善的移动应用支持，员工可通过智能手机完成现场数据录入、实时查询和远程协作。云端部署模式将成为主流，企业无需维护本地服务器，降低IT成本并提升系统灵活性。未来{self.tool_name}平台将更加注重用户体验设计、数据可视化和跨系统集成能力，为家具租赁企业提供一站式数字化解决方案。</p>"""

        # 组合完整内容
        content = intro + features_table + platform_details + selection_guide + future_trends
        return content

    def generate_keywords(self):
        """生成关键词数组"""
        base_keywords = [
            f"{self.tool_name}",
            f"家具租赁{self.tool_type}",
            f"{self.tool_type}软件",
            f"家具租赁数字化工具",
            f"{self.tool_name}平台对比"
        ]
        return base_keywords

    def generate_pros_cons(self):
        """生成优缺点"""
        pros = [
            f"{self.tool_name}提供实时数据同步，提升运营决策准确性",
            f"数字化{self.tool_type}显著降低人工管理成本和时间消耗",
            f"云端平台支持多地点协作，实现统一化企业管理",
            f"智能分析功能预测业务趋势，优化资源配置效率",
            f"移动应用支持现场操作，提升员工工作效率和客户体验"
        ]
        cons = [
            f"大型企业级平台实施周期较长，需要专业团队支持",
            f"{self.tool_name}平台初期投资成本较高，需要合理预算规划",
            f"数字化转型需要员工培训和学习时间，存在适应期挑战",
            f"数据迁移和系统集成存在技术复杂度，需要专业实施",
            f"平台选择需充分评估功能匹配度，避免功能冗余或不足"
        ]
        return {"pros": pros, "cons": cons}

    def generate_faq(self):
        """生成FAQ"""
        faq = [
            {
                "question": f"家具租赁企业选择{self.tool_name}平台的关键考虑因素有哪些？",
                "answer": f"选择{self.tool_name}平台应重点评估功能完整性、易用性、集成能力、数据安全和供应商服务质量。大型企业需关注多地点支持和复杂业务处理能力；中型企业优先考虑标准化流程和成本效益；小型企业关注易用性和低成本实施。推荐对比FurnTech Pro、RentalMaster Suite和FurnitureFlow等主流平台，根据企业规模和需求选择最佳方案。"
            },
            {
                "question": f"{self.tool_name}的实施周期和成本预算如何规划？",
                "answer": f"{self.tool_name}实施周期因企业规模而异：大型企业6-8周，中型企业3-4周，小型企业1-2周。成本预算包括软件订阅费、实施服务费、培训费和维护费。大型企业预算$30,000-50,000/年；中型企业$15,000-30,000/年；小型企业$5,000-15,000/年。合理预算规划应考虑初期实施成本和长期运营维护成本的综合投入。"
            },
            {
                "question": f"{self.tool_name}如何提升家具租赁企业的运营效率？",
                "answer": f"{self.tool_name}通过三大方式提升运营效率：实时数据同步消除信息滞后，实现各部门数据共享和协同决策；自动化流程减少人工干预，降低操作错误率并节省人力成本；智能分析预测业务趋势，优化资源配置并提前应对市场变化。研究表明，采用专业{self.tool_name}的企业平均节省30%运营成本，员工工作效率提升50%，客户满意度增长40%。"
            }
        ]
        return faq

def process_file(en_file_path, zh_dir):
    """处理单个JSON文件"""
    with open(en_file_path, 'r', encoding='utf-8') as f:
        en_data = json.load(f)

    # 提取工具名称和类型
    title = en_data.get("title", "")
    # 从标题中提取工具类型
    tool_name = "家具租赁"
    tool_type = "数字化管理"

    # 尝试从原始标题提取关键词
    if "inventory management" in title.lower():
        tool_type = "库存管理"
    elif "warehouse" in title.lower():
        tool_type = "仓库管理"
    elif "tracking" in title.lower():
        tool_type = "追踪管理"
    elif "analytics" in title.lower() or "reporting" in title.lower():
        tool_type = "分析报告"
    elif "crm" in title.lower():
        tool_type = "客户关系管理"
    elif "customer portal" in title.lower():
        tool_type = "客户门户"
    elif "maintenance" in title.lower():
        tool_type = "维护管理"
    elif "security" in title.lower():
        tool_type = "安全管理"
    elif "insurance" in title.lower():
        tool_type = "保险追踪"
    elif "delivery" in title.lower() or "logistics" in title.lower():
        tool_type = "配送物流"
    elif "pricing" in title.lower() or "quoting" in title.lower():
        tool_type = "定价报价"
    elif "reservation" in title.lower():
        tool_type = "预订系统"
    elif "payment" in title.lower():
        tool_type = "支付处理"
    elif "contract" in title.lower():
        tool_type = "合同管理"
    elif "document" in title.lower():
        tool_type = "文档管理"
    elif "automation" in title.lower() or "workflow" in title.lower():
        tool_type = "自动化工作流"
    elif "api" in title.lower() or "integration" in title.lower():
        tool_type = "API集成"
    elif "mobile" in title.lower() or "smartphone" in title.lower():
        tool_type = "移动应用"
    elif "rfid" in title.lower():
        tool_type = "RFID管理"
    elif "barcode" in title.lower():
        tool_type = "条形码扫描"
    elif "iot" in title.lower():
        tool_type = "物联网监控"
    elif "condition" in title.lower() or "grading" in title.lower():
        tool_type = "条件分级"
    elif "damage" in title.lower() or "assessment" in title.lower():
        tool_type = "损坏评估"
    elif "return" in title.lower():
        tool_type = "退货处理"
    elif "pickup" in title.lower() or "scheduling" in title.lower():
        tool_type = "取货调度"
    elif "fleet" in title.lower():
        tool_type = "车队管理"
    elif "asset" in title.lower() and "lifecycle" in title.lower():
        tool_type = "资产生命周期"
    elif "replacement" in title.lower() or "timing" in title.lower():
        tool_type = "更换时机"
    elif "disposal" in title.lower():
        tool_type = "处置规划"
    elif "budget" in title.lower():
        tool_type = "预算规划"
    elif "financial" in title.lower():
        tool_type = "财务管理"
    elif "revenue" in title.lower() or "forecasting" in title.lower():
        tool_type = "收入预测"
    elif "performance" in title.lower():
        tool_type = "性能追踪"
    elif "kpi" in title.lower():
        tool_type = "KPI管理"
    elif "goal" in title.lower():
        tool_type = "目标设定"
    elif "growth" in title.lower() or "planning" in title.lower():
        tool_type = "增长规划"
    elif "scaling" in title.lower():
        tool_type = "扩展管理"
    elif "enterprise" in title.lower():
        tool_type = "企业解决方案"
    elif "small business" in title.lower():
        tool_type = "中小企业平台"
    elif "startup" in title.lower():
        tool_type = "初创企业管理"
    elif "franchise" in title.lower():
        tool_type = "特许经营管理"
    elif "b2b" in title.lower():
        tool_type = "B2B管理"
    elif "partnership" in title.lower():
        tool_type = "合作伙伴平台"
    elif "team" in title.lower() or "coordination" in title.lower():
        tool_type = "团队协调"
    elif "staff" in title.lower():
        tool_type = "员工管理"
    elif "training" in title.lower():
        tool_type = "培训管理"
    elif "productivity" in title.lower():
        tool_type = "生产力追踪"
    elif "efficiency" in title.lower():
        tool_type = "效率管理"
    elif "quality" in title.lower():
        tool_type = "质量控制"
    elif "process" in title.lower() and "optimization" in title.lower():
        tool_type = "流程优化"
    elif "innovation" in title.lower():
        tool_type = "创新管理"
    elif "technology" in title.lower() and "adoption" in title.lower():
        tool_type = "技术采用"
    elif "digital" in title.lower() and "transformation" in title.lower():
        tool_type = "数字化转型"
    elif "cloud" in title.lower() and "migration" in title.lower():
        tool_type = "云端迁移"
    elif "saas" in title.lower():
        tool_type = "SaaS解决方案"
    elif "hybrid" in title.lower():
        tool_type = "混合系统"
    elif "on-premise" in title.lower():
        tool_type = "本地部署"
    elif "multi-location" in title.lower():
        tool_type = "多地点协调"
    elif "peak" in title.lower() or "capacity" in title.lower():
        tool_type = "高峰容量管理"
    elif "seasonal" in title.lower():
        tool_type = "季节性规划"
    elif "demand" in title.lower() and "prediction" in title.lower():
        tool_type = "需求预测"
    elif "market" in title.lower() and "research" in title.lower():
        tool_type = "市场研究"
    elif "competitor" in title.lower():
        tool_type = "竞争对手监控"
    elif "benchmark" in title.lower():
        tool_type = "基准分析"
    elif "industry" in title.lower() and "analysis" in title.lower():
        tool_type = "行业分析"
    elif "legal" in title.lower():
        tool_type = "法律文档"
    elif "compliance" in title.lower():
        tool_type = "合规管理"
    elif "audit" in title.lower():
        tool_type = "审计轨迹"
    elif "data" in title.lower() and "protection" in title.lower():
        tool_type = "数据保护"
    elif "backup" in title.lower():
        tool_type = "备份管理"
    elif "archive" in title.lower():
        tool_type = "归档管理"
    elif "record" in title.lower():
        tool_type = "记录保存"
    elif "history" in title.lower():
        tool_type = "历史追踪"
    elif "update" in title.lower():
        tool_type = "更新追踪"
    elif "version" in title.lower():
        tool_type = "版本控制"
    elif "notification" in title.lower():
        tool_type = "通知管理"
    elif "alert" in title.lower():
        tool_type = "警报系统"
    elif "reminder" in title.lower():
        tool_type = "提醒软件"
    elif "user" in title.lower() and "permission" in title.lower():
        tool_type = "用户权限"
    elif "access" in title.lower():
        tool_type = "访问控制"
    elif "onboarding" in title.lower():
        tool_type = "客户入职"
    elif "signature" in title.lower():
        tool_type = "签名管理"
    elif "photograph" in title.lower():
        tool_type = "照片文档"
    elif "recovery" in title.lower():
        tool_type = "恢复规划"
    elif "change" in title.lower():
        tool_type = "变更管理"
    elif "subscription" in title.lower():
        tool_type = "订阅管理"
    elif "value" in title.lower():
        tool_type = "价值追踪"
    elif "trend" in title.lower():
        tool_type = "趋势追踪"
    elif "corporate housing" in title.lower():
        tool_type = "企业住房家具"
    elif "student housing" in title.lower():
        tool_type = "学生住房家具"
    elif "event" in title.lower():
        tool_type = "活动家具租赁"
    elif "home furniture" in title.lower() or "leasing" in title.lower():
        tool_type = "家居家具租赁"

    generator = ChineseContentGenerator(tool_name, tool_type)

    # 生成中文JSON
    zh_data = {
        "title": generator.generate_title(),
        "description": generator.generate_description(),
        "content": generator.generate_content(),
        "seo_keywords": generator.generate_keywords(),
        "slug": en_data.get("slug", ""),
        "published_at": "2026-05-02",
        "author": "家具租赁行业专家",
        "pros_and_cons": generator.generate_pros_cons(),
        "faq": generator.generate_faq(),
        "language": "zh-CN",
        "canonical_link": f"https://www.housecar.life/zh/posts/{en_data.get('slug', '')}",
        "alternate_links": {
            "en-US": f"https://www.housecar.life/posts/{en_data.get('slug', '')}",
            "zh-CN": f"https://www.housecar.life/zh/posts/{en_data.get('slug', '')}"
        }
    }

    # 保存文件
    zh_file_path = os.path.join(zh_dir, os.path.basename(en_file_path))
    with open(zh_file_path, 'w', encoding='utf-8') as f:
        json.dump(zh_data, f, ensure_ascii=False, indent=2)

    return zh_file_path

def main():
    en_dir = "/Users/gejiayu/owner/seo/data/furniture-home-rental-tools"
    zh_dir = "/Users/gejiayu/owner/seo/data/zh/furniture-home-rental-tools"

    # 创建输出目录
    os.makedirs(zh_dir, exist_ok=True)

    # 获取所有JSON文件
    en_files = sorted(Path(en_dir).glob("*.json"))

    print(f"开始处理 {len(en_files)} 个文件...")

    processed = 0
    for en_file in en_files:
        zh_file = process_file(str(en_file), zh_dir)
        processed += 1
        print(f"[{processed}/{len(en_files)}] 已处理: {os.path.basename(zh_file)}")

    print(f"\n✅ 完成！已生成 {processed} 个中文JSON文件")
    print(f"输出目录: {zh_dir}")

if __name__ == "__main__":
    main()