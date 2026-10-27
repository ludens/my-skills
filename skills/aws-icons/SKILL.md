---
name: aws-icons
description: Use when AWS 서비스가 포함된 구조도·아키텍처 다이어그램을 그릴 때, 또는 AWS Architecture Icons의 정확한 파일명·카테고리·크기·SVG 다운로드·삽입 방법이 필요할 때. EC2, S3, Lambda, RDS, DynamoDB, VPC, IAM, CloudFront, Route 53 같은 공식 아이콘의 slug와 경로를 찾는 경우를 포함한다. / Triggers: draw AWS architecture diagram SVG, official AWS service icons download, find EC2 S3 Lambda icon slug and path
---

# AWS Icons

AWS Architecture Icons(공식 아이콘 세트)를 찾고, 내려받고, SVG 구조도에 삽입할 때 참조하는 카탈로그.

## 소스

| 항목 | 값 |
| --- | --- |
| 아이콘 페이지 | <https://aws.amazon.com/architecture/icons/> |
| 에셋 패키지 ZIP | `https://d1.awsstatic.com/onedam/marketing-channels/website/aws/en_US/architecture/approved/architecture-icons/Asset-Package_07312025.49d3aab7f9e6131e51ade8f7c6c8b961ee7d3bb1.zip` |
| 갱신 주기 | 분기별: Q1(1월 말)·Q2(4월 말)·Q3(7월 말), Q4 없음 |

아이콘은 개별 URL이 없고 분기 ZIP 하나로 배포된다. ZIP 안에는 SVG·PNG·PPT·PDF가 섞여 있다. 전체 서비스 목록은 [references/icon-catalog.md](references/icon-catalog.md)에 있다.

## 경로 규칙

```
Architecture-Service-Icons_<YYYYMMDD>/Arch_<Category>/<size>/Arch_<Name>_<size>.svg
Architecture-Group-Icons_<YYYYMMDD>/<Name>_32.svg
Resource-Icons_<YYYYMMDD>/Res_<Category>/Res_<Name>_48.svg
Category-Icons_<YYYYMMDD>/Arch-Category_<size>/Arch-Category_<Category>_<size>.svg
```

- 서비스 아이콘: `Arch_` 접두, `Amazon-` 또는 `AWS-`로 시작하는 서비스명, `_<size>.svg` 접미. 모든 서비스가 16/32/48/64 네 크기를 갖는다.
- `_<size>`는 슬롯 크기이고 실제 SVG viewBox는 아이콘 계열마다 다르다. 다이어그램에 48px 노드를 쓸 때 서비스 아이콘은 `_48.svg`(viewBox 64)를 골라 `<use width="48" height="48">`으로 스케일한다.

| 아이콘 계열 | viewBox |
| --- | --- |
| 서비스 `Arch_*_16` | `0 0 24 24` |
| 서비스 `Arch_*_32` | `0 0 40 40` |
| 서비스 `Arch_*_48` | `0 0 64 64` |
| 서비스 `Arch_*_64` | `0 0 80 80` |
| 리소스 `Res_*_48` | `0 0 48 48` |
| 그룹 `*_32` | `0 0 40 40` |
| 카테고리 `Arch-Category_*_48` | `0 0 74 74` |

## 빠른 선택

기본은 서비스 아이콘 48px(`Arch_<Category>/48/Arch_<Name>_48.svg`). 로드 밸런서 종류와 같은 하위 리소스는 `Res_` 아이콘을 쓴다.

| 구조도 노드 | 경로 |
| --- | --- |
| 인터넷 / 사용자 | AWS 아이콘 없음. 중립 지구본·사람 도형을 그린다. |
| AWS 클라우드 경계 | `Architecture-Group-Icons_*/AWS-Cloud_32.svg` |
| 리전 | `Architecture-Group-Icons_*/Region_32.svg` |
| 기업·온프레미스 | `Architecture-Group-Icons_*/Corporate-data-center_32.svg` |
| VPC | `Arch_Networking-Content-Delivery/48/Arch_Amazon-Virtual-Private-Cloud_48.svg` |
| 서브넷(공개/비공개) | `Architecture-Group-Icons_*/Public-subnet_32.svg`, `Private-subnet_32.svg` |
| DNS / Route 53 | `Arch_Networking-Content-Delivery/48/Arch_Amazon-Route-53_48.svg` |
| CDN / CloudFront | `Arch_Networking-Content-Delivery/48/Arch_Amazon-CloudFront_48.svg` |
| 로드 밸런서(공통) | `Arch_Networking-Content-Delivery/48/Arch_Elastic-Load-Balancing_48.svg` |
| ALB | `Resource-Icons_*/Res_Networking-Content-Delivery/Res_Elastic-Load-Balancing_Application-Load-Balancer_48.svg` |
| NLB / GWLB / CLB | 같은 폴더의 `..._Network-Load-Balancer` / `..._Gateway-Load-Balancer` / `..._Classic-Load-Balancer` |
| API Gateway | `Arch_Networking-Content-Delivery/48/Arch_Amazon-API-Gateway_48.svg` |
| Direct Connect | `Arch_Networking-Content-Delivery/48/Arch_AWS-Direct-Connect_48.svg` |
| Transit Gateway | `Arch_Networking-Content-Delivery/48/Arch_AWS-Transit-Gateway_48.svg` |
| EC2 | `Arch_Compute/48/Arch_Amazon-EC2_48.svg` |
| Auto Scaling | `Arch_Compute/48/Arch_Amazon-EC2-Auto-Scaling_48.svg` |
| Lambda | `Arch_Compute/48/Arch_AWS-Lambda_48.svg` |
| ECS / EKS / Fargate / ECR | `Arch_Containers/48/Arch_Amazon-Elastic-Container-Service_48.svg` 등 |
| S3 | `Arch_Storage/48/Arch_Amazon-Simple-Storage-Service_48.svg` |
| EBS | `Arch_Storage/48/Arch_Amazon-Elastic-Block-Store_48.svg` |
| EFS | `Arch_Storage/48/Arch_Amazon-EFS_48.svg` |
| S3 Glacier | `Arch_Storage/48/Arch_Amazon-Simple-Storage-Service-Glacier_48.svg` |
| RDS | `Arch_Database/48/Arch_Amazon-RDS_48.svg` |
| Aurora | `Arch_Database/48/Arch_Amazon-Aurora_48.svg` |
| DynamoDB | `Arch_Database/48/Arch_Amazon-DynamoDB_48.svg` |
| ElastiCache | `Arch_Database/48/Arch_Amazon-ElastiCache_48.svg` |
| Redshift | `Arch_Analytics/48/Arch_Amazon-Redshift_48.svg` |
| IAM | `Arch_Security-Identity-Compliance/48/Arch_AWS-Identity-and-Access-Management_48.svg` |
| Cognito | `Arch_Security-Identity-Compliance/48/Arch_Amazon-Cognito_48.svg` |
| KMS | `Arch_Security-Identity-Compliance/48/Arch_AWS-Key-Management-Service_48.svg` |
| WAF / Shield | `Arch_Security-Identity-Compliance/48/Arch_AWS-WAF_48.svg`, `.../Arch_AWS-Shield_48.svg` |
| Secrets Manager | `Arch_Security-Identity-Compliance/48/Arch_AWS-Secrets-Manager_48.svg` |
| SQS | `Arch_App-Integration/48/Arch_Amazon-Simple-Queue-Service_48.svg` |
| SNS | `Arch_App-Integration/48/Arch_Amazon-Simple-Notification-Service_48.svg` |
| EventBridge | `Arch_App-Integration/48/Arch_Amazon-EventBridge_48.svg` |
| Step Functions | `Arch_App-Integration/48/Arch_AWS-Step-Functions_48.svg` |
| CloudWatch | `Arch_Management-Governance/48/Arch_Amazon-CloudWatch_48.svg` |
| CloudFormation | `Arch_Management-Governance/48/Arch_AWS-CloudFormation_48.svg` |
| CloudTrail | `Arch_Management-Governance/48/Arch_AWS-CloudTrail_48.svg` |
| SageMaker | `Arch_Artificial-Intelligence/48/Arch_Amazon-SageMaker-AI_48.svg` |
| Bedrock | `Arch_Artificial-Intelligence/48/Arch_Amazon-Bedrock_48.svg` |

카테고리 디렉터리명은 표기 이름과 다를 수 있다. `Arch_Database`(단수), `Arch_App-Integration`(짧게), 리소스는 `Res_Application-Integration`(풀네임), `Res_IoT`(짧게). 헷갈리면 `fetch-icons.sh --list`로 확인한다.

## 카테고리 색

아이콘은 카테고리색 타일 + 흰색 글리프로 구성돼 있고, 색은 파일 안에 박혀 있다. 재색칠하지 않는다.

| 카테고리 | 색 |
| --- | --- |
| Compute·Containers·Blockchain·Media·Quantum | `#ED7100` |
| Storage·Cloud-Financial-Management·IoT | `#7AA116` |
| Database·Developer-Tools·Customer-Enablement·Satellite | `#C925D1` |
| Networking-Content-Delivery·Analytics·Games | `#8C4FFF` |
| Security-Identity-Compliance·Business-Applications·Front-End | `#DD344C` |
| App-Integration·Management-Governance | `#E7157B` |
| AI·End-User-Computing·Migration | `#01A88D` |

## 다운로드

```bash
# 하나
bash scripts/fetch-icons.sh assets/aws-icons amazon-ec2

# 여러 개
bash scripts/fetch-icons.sh assets/aws-icons amazon-ec2 aws-lambda amazon-simple-storage-service amazon-dynamodb

# 검색(경로 확인)
bash scripts/fetch-icons.sh assets/aws-icons --list ec2

# 특정 크기 / 전체 서비스 아이콘
AWS_ICONS_SIZE=32 bash scripts/fetch-icons.sh assets/aws-icons amazon-ec2
bash scripts/fetch-icons.sh assets/aws-icons --all
```

`fetch-icons.sh`는 ZIP을 `~/.cache/aws-icons`에 캐시하고, 모호한 slug(예: `ec2` → EC2·EC2-Auto-Scaling·EC2-Image-Builder)는 후보를 나열하고 실패한다. 전체 이름(`amazon-ec2`, `aws-lambda`)을 쓰면 정확히 추출된다. 리소스 아이콘도 전체 이름으로 추출한다.

```bash
# ALB 리소스 아이콘 (Res_ 계열)
bash scripts/fetch-icons.sh assets/aws-icons elastic-load-balancing-application-load-balancer
```

## SVG에 삽입

AWS 아이콘은 이미 색이 입혀진 타일이라, cloudflare 아이콘과 달리 `fill`을 다시 주지 않는다. 심볼로 넣고 `use`로 참조한다.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 160">
  <defs>
    <!-- Arch_Amazon-EC2_48.svg에서 <?xml?>, 바깥 <svg>, <title>, id 속성을 제거한 내부 -->
    <symbol id="aws-ec2" viewBox="0 0 64 64">
      <g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
        <g fill="#ED7100"><rect x="0" y="0" width="64" height="64"/></g>
        <path d="..." fill="#FFFFFF"/>
      </g>
    </symbol>
  </defs>

  <use href="#aws-ec2" x="52" y="63" width="48" height="48"/>
  <text x="76" y="140" font-size="12" fill="#334155">EC2</text>
</svg>
```

삽입 규칙:

1. 바깥 `<svg>`의 `viewBox`를 `<symbol viewBox="...">`로 옮긴다. `_48.svg`는 `viewBox="0 0 64 64"`다.
2. `<title>`과 모든 `id="..."` 속성을 제거한다. AWS SVG의 `id`는 `Rectangle`, `Fill-1`, `Icon-Architecture/48/...` 같은 레이블일 뿐 참조되지 않아, 여러 아이콘을 인라인하면 id가 충돌한다. 단, `url(#clip0_...)`처럼 실제로 참조되는 clipPath id는 남기고 심볼마다 접두사를 붙인다.
3. `fill`은 파일 안에 이미 있다(타일 색 + 흰 글리프). 다시 지정하지 않는다.
4. `<use>`에 `width`/`height`를 주고 아이콘을 48px 슬롯에 맞춘다. 기본 `preserveAspectRatio="xMidYMid meet"`가 비율을 지킨다.

심볼 생성은 스크립트로 처리한다.

```bash
python3 scripts/build-sprite.py --dir assets/aws-icons \
  --out assets/aws-sprite.svg Arch_Amazon-EC2_48.svg Arch_AWS-Lambda_48.svg

# <symbol> 블록만 출력해 기존 <defs>에 붙이기
python3 scripts/build-sprite.py --dir assets/aws-icons --fragment \
  Arch_Amazon-EC2_48.svg Arch_AWS-Lambda_48.svg
```

`build-sprite.py`는 레이블 id를 제거하고 clipPath id만 `aws-<slug>__` 접두사로 네임스페이스한다.

## 배치

- 아이콘은 48px가 기본. 같은 구조도 안에서 크기를 통일한다.
- 아이콘만 두지 말고 서비스명을 함께 적는다. `RDS`·`Aurora`·`DynamoDB`는 글자 없이는 구분이 어렵다.
- AWS 클라우드 경계는 `AWS-Cloud_32.svg`로 점선 박스를 그리고, VPC·서브넷은 그 안에 둔다.
- 리소스 아이콘(`Res_*`, 하위 구성요소)을 서비스 아이콘(`Arch_*`)과 같은 크기로 섞지 않는다. 리소스는 보조 레이블용으로 작게 쓴다.
- 화살표가 타일을 관통하지 않게 한다. 아이콘과 텍스트 사이는 8–12px.
- 다이어그램이 흰 배경이면 기본 타일을, 어두운 배경이면 `*_Dark` 변형(제공되는 아이콘만)을 쓴다.

## 자주 틀리는 것

| 오해·증상 | 실제 |
| --- | --- |
| 아이콘을 개별 URL로 받는다 | 개별 URL이 없다. 분기 ZIP에서 `fetch-icons.sh`로 추출한다. |
| `_48.svg`의 viewBox가 48이다 | viewBox는 64. `_16→24`, `_32→40`, `_48→64`, `_64→80`. |
| 카테고리 디렉터리가 `Arch_Databases`다 | `Arch_Database`(단수)다. |
| ALB 전용 아이콘이 없다 | `Res_Elastic-Load-Balancing_Application-Load-Balancer_48.svg`가 있다. 공통은 `Arch_Elastic-Load-Balancing`. |
| IAM 파일명이 `IAM`이다 | `Arch_AWS-Identity-and-Access-Management`이다. |
| S3 파일명이 `S3`다 | `Arch_Amazon-Simple-Storage-Service`다. |
| 아이콘을 단색으로 재색칠한다 | 색(카테고리 타일 + 흰 글리프)이 파일에 박혀 있다. 그대로 둔다. |
| 인라인한 `id="Rectangle"`을 남긴다 | 여러 아이콘에서 충돌한다. `build-sprite.py`가 제거/네임스페이스한다. |
| 패키지 버전을 추측해 적는다 | 파일명의 `_YYYYMMDD`(예: `_07312025`)가 릴리스다. 페이지의 다운로드 링크에서 실제값을 확인한다. |

## 검증

```bash
# ZIP 안에서 실제 경로 확인
bash scripts/fetch-icons.sh assets/aws-icons --list ec2

# 추출한 SVG가 유효한지(타일+글리프, viewBox)
head -c 300 assets/aws-icons/Arch_Amazon-EC2_48.svg

# 결과 구조도 XML 검증
xmllint --noout diagram.svg
```

브라우저나 `qlmanage`로 실제 렌더링을 확인한다. ImageMagick의 내장 SVG 렌더러는 일부 path·폰트를 처리하지 못하므로 판정 기준으로 쓰지 않는다.

이 카탈로그는 2025-07-31 스냅샷(`_07312025`)이다. 분기마다 아이콘이 갱신되므로, 중요한 산출물이면 내려받은 SVG를 저장소에 커밋해 고정한다.
