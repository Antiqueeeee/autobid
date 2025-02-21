from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from bidding_workflow import BiddingWorkflow
import logging
from config import Config
import json
from app_params import OutlineRequest, ContentRequest

app = FastAPI()
logger = logging.getLogger(__name__)

@app.post("/generate_outline")
async def generate_outline(request: OutlineRequest):
    async with BiddingWorkflow() as workflow:
        try:
            logger.info("Starting outline generation")
            
            # # Load input files
            # logger.info("Loading input files")
            # workflow.load_input_files()
            
            # Generate outline with parameters
            logger.info("Generating outline")
            outline_json = await workflow.generate_outline(
                tech_content=request.tech_content,
                score_content=request.score_content
            )
            if not outline_json:
                logger.error("Failed to generate outline")
                raise HTTPException(status_code=500, detail="Failed to generate outline")
                
            logger.info("Successfully generated outline")
            
            # Parse outline
            logger.info("Parsing outline JSON")
            workflow.outline = workflow.parse_outline_json(outline_json)
            
            # Save outline
            logger.info("Saving outline")
            workflow.save_outline()
            
            logger.info("Outline generation completed successfully")
            return JSONResponse(content={
                "status": "success",
                "outline": workflow.outline.to_dict()
            })
        except Exception as e:
            logger.error(f"Error in generate_outline: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_content")
async def generate_content(request: ContentRequest):
    workflow = BiddingWorkflow()
    try:
        # # Load input files
        # workflow.load_input_files()
        
        # # Load saved outline
        # with open(Config.OUTLINE_DIR / 'outline.json', 'r', encoding='utf-8') as f:
        #     outline_dict = json.load(f)
        #     workflow.outline = workflow.parse_outline_json(outline_dict)
        
        # outline_dict = json.loads(request.outline)
        workflow.outline = workflow.parse_outline_json(request.outline)
        
        
        # success = await workflow.generate_full_content_async(outline=workflow.outline)
        content = await workflow.generate_full_content_async(outline=workflow.outline)
        if content:
            return JSONResponse(content={"status": "success", "content": content})
        else:
            raise HTTPException(status_code=500, detail="Content generation failed")
    except Exception as e:
        logger.error(f"Error in generate_content: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await workflow.llm_client.close()

@app.post("/generate_document")
async def generate_document():
    workflow = BiddingWorkflow()
    try:
        # # Load input files
        # workflow.load_input_files()
        
        # Load outline
        with open(Config.OUTLINE_DIR / 'outline.json', 'r', encoding='utf-8') as f:
            outline_dict = json.load(f)
            workflow.outline = workflow.parse_outline_json(outline_dict)
        
        # Generate full content
        success = await workflow.generate_full_content_async()
        if not success:
            raise HTTPException(status_code=500, detail="Failed to generate content")
        
        return JSONResponse(content={
            "status": "success",
            "message": "Document generated successfully"
        })
        
    except Exception as e:
        logger.error(f"Error generating document: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await workflow.llm_client.close()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=Config.SERVER_NAME, port=Config.SERVER_PORT)

