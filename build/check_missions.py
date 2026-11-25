# 실전 연습장 미션 판정 점검 (로컬 서버 8765번 필요). 직접 조작하기 전에는 미션이 판정되지 않아야 하고, 조작하면 판정돼야 한다.
import asyncio, json
from playwright.async_api import async_playwright
async def setr(page,sc,name,v):
    await page.evaluate("([sc,n,v])=>{const e=document.querySelector('#'+sc+' [name='+n+']');if(e.type==='checkbox'){e.checked=v;}else e.value=v;e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));}",[sc,name,v])
async def done(page,sc): return await page.evaluate("sc=>[...document.querySelectorAll('#'+sc+' .missions li')].map(l=>l.classList.contains('done'))",sc)
TARGETS={'retro':[10,50,55,20,10,70],'sd':[85,35,5,75,10,85],'ink':[80,90,60,10,50,0],'toy':[95,10,5,10,95,80],'graphic':[55,75,95,25,40,15],'sketch':[85,35,60,40,0,0],'modern':[95,25,50,30,15,85]}
async def main():
    ok=True
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
        page=await b.new_page();await page.route('**/fonts.g*/**',lambda r: r.abort())
        await page.goto("http://localhost:8765/practice/index.html#bench");await page.wait_for_timeout(800)
        r0=await done(page,'bench');print('bench before',r0);ok&=not any(r0)
        for t,v in TARGETS.items():
            await setr(page,'bench','target',t)
            for n,x in zip(['era','line','real','exag','media','color'],v): await setr(page,'bench',n,x)
        r=await done(page,'bench');print('bench after',r);ok&=all(r)
        await page.click('.tabs button[data-t=sort]')
        r0=await done(page,'sort');print('sort before',r0);ok&=not any(r0)
        D=json.loads(await page.text_content('#style-pts'));G=D['groups']
        for _ in range(200):
            sym=(await page.text_content('#sort .sym')).replace('카드: ','').replace('  [경계 카드]','')
            pt=[x for x in D['pts'] if x['d']==sym][0]
            # 아직 안 쓴 군집이 정답이면 그쪽을 고른다
            used=await page.evaluate("()=>[...document.querySelectorAll('#sort .g2 text')].filter(t=>t.textContent.includes('✓')).map(t=>t.textContent.replace(' ✓',''))")
            choice=G[str(pt['alt'])] if pt['alt'] and G[str(pt['alt'])] not in used else G[str(pt['g'])]
            await page.click(f"#sort .sortopts button:text-is('{choice}')");await page.wait_for_timeout(420)
            if all(await done(page,'sort')): break
        r=await done(page,'sort');print('sort after',r);ok&=all(r)
        await page.click('.tabs button[data-t=workshop]')
        r0=await done(page,'workshop');print('workshop before',r0);ok&=not any(r0)
        await setr(page,'workshop','job','sticker')
        for n,v in [('who','haru'),('keep',True),('axis','sd'),('axis2',''),('heads','sd'),('exag','one'),('desc','feat'),('adult',True),('notext',True)]: await setr(page,'workshop',n,v)
        await setr(page,'workshop','axis','ink');await setr(page,'workshop','heads','std')
        r=await done(page,'workshop');print('workshop after',r);ok&=all(r)
        await page.click('.tabs button[data-t=desk]')
        SYM=['머리띠와 리본이 사라져','한 번에 요청해','셀도 수채도','아이처럼 보인다','한가운데에 눈이','하트를 모두 키워','생김새를 놀리는','뜻 없는 글씨와 도장']
        CA=['고정값 빠짐','두 축 동시 변경','군집 사이 어중간','SD 나이 쏠림','SD 부위 그대로','과장 여러 곳','외모 조롱','가짜 글씨·작품 이름']
        r0=await done(page,'desk');print('desk before',r0);ok&=not any(r0)
        for _ in range(70):
            sym=await page.text_content('#desk .sym');k=[i for i,s in enumerate(SYM) if s in sym][0]
            await page.click(f"#desk .deskopts button:text-is('{CA[k]}')");await page.wait_for_timeout(560)
            if all(await done(page,'desk')): break
        r=await done(page,'desk');print('desk after',r);ok&=all(r)
        await b.close()
    print('미션 점검 통과' if ok else '미션 점검 실패')
asyncio.run(main())
