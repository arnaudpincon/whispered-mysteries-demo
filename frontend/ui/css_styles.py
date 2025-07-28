#!/usr/bin/env python3
"""CSS styles for the detective game frontend - WITH RESPONSIVE FONT SIZING"""

from ..core.constants import CSSClasses, UIConstants

CSS_STYLES = f"""
        @import url('https://fonts.googleapis.com/css2?family=Dobra:wght@400;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');

        /* Root font size responsive - base for all rem units */
        :root {{
            /* Base font size adapts to screen width */
            font-size: clamp(10px, 1.3vw, 16px);
            
            /* Font scale variables for different screen sizes */
            --font-scale-small: 0.6;
            --font-scale-medium: 0.8;
            --font-scale-large: 1.0;
            --font-scale-xlarge: 1.2;
        }}

        html, body, .gradio-container {{
            font-family: 'Dobra', sans-serif !important;
            height: 90% !important;
            margin: 0;
            padding: 0;
            font-size: 1rem; /* Uses the responsive root font-size */
        }}

        /* Responsive font sizing based on screen width */
        @media screen and (max-width: 480px) {{
            :root {{
                font-size: clamp(10px, 3vw, 14px);
            }}
            
            html, body, .gradio-container {{
                font-size: calc(1rem * var(--font-scale-small));
            }}
        }}

        @media screen and (min-width: 481px) and (max-width: 768px) {{
            :root {{
                font-size: clamp(12px, 2.5vw, 16px);
            }}
            
            html, body, .gradio-container {{
                font-size: calc(1rem * var(--font-scale-medium));
            }}
        }}

        @media screen and (min-width: 769px) and (max-width: 1024px) {{
            :root {{
                font-size: clamp(14px, 2vw, 18px);
            }}
            
            html, body, .gradio-container {{
                font-size: calc(1rem * var(--font-scale-medium));
            }}
        }}

        @media screen and (min-width: 1025px) and (max-width: 1440px) {{
            :root {{
                font-size: clamp(16px, 1.8vw, 20px);
            }}
            
            html, body, .gradio-container {{
                font-size: calc(1rem * var(--font-scale-large));
            }}
        }}

        @media screen and (min-width: 1441px) {{
            :root {{
                font-size: clamp(18px, 1.5vw, 24px);
            }}
            
            html, body, .gradio-container {{
                font-size: calc(1rem * var(--font-scale-xlarge));
            }}
        }}

        #{CSSClasses.MAIN_CONTAINER} {{
            height: 100%;
        }}

        #{CSSClasses.SCENE_IMG} {{
            height: {UIConstants.SCENE_IMAGE_HEIGHT} !important;
            object-fit: contain;
        }}

        #{CSSClasses.MAP_IMG} {{
            height: {UIConstants.MAP_IMAGE_HEIGHT} !important;
            object-fit: contain;
        }}

        #{CSSClasses.INVENTORY_TEXT} {{
            height: {UIConstants.INVENTORY_HEIGHT} !important;
            overflow-y: auto !important;
            padding: 0.6rem;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-family: "Libre Baskerville", serif !important;
            font-size: 1rem; /* Responsive font size */
            line-height: 1.4;
        }}

        #{CSSClasses.CHARACTER_IMG} {{
            height: {UIConstants.CHARACTER_IMAGE_HEIGHT} !important;
            object-fit: contain;
        }}

        #{CSSClasses.NARRATIVE_BOX} {{
            flex-grow: 0.65 !important;
            height: {UIConstants.CHATBOT_HEIGHT};
            display: grid;
            font-family: 'Libre Baskerville', serif !important;
            font-size: 1rem; /* Responsive font size */
        }}

        /* Chat interface responsive typography */
        .gradio-container .prose {{
            font-size: 1rem !important;
            line-height: 1.5 !important;
        }}

        .gradio-container .prose p {{
            font-size: 1rem !important;
            margin-bottom: 1rem !important;
        }}

        .gradio-container .prose h1 {{
            font-size: 1.5rem !important;
        }}

        .gradio-container .prose h2 {{
            font-size: 1.3rem !important;
        }}

        .gradio-container .prose h3 {{
            font-size: 1.1rem !important;
        }}

        /* Button responsive typography */
        button {{
            font-size: 0.9rem !important;
            padding: 0.5rem 1rem !important;
        }}

        @media screen and (max-width: 768px) {{
            button {{
                font-size: 0.8rem !important;
                padding: 0.4rem 0.8rem !important;
            }}
        }}
        
        /* Hide Gradio default footer elements */
        footer {{
            display: none !important;
        }}
        
        .gradio-container .footer,
        .gradio-container > .footer {{
            display: none !important;
        }}
        
        .hide-input .wrap.svelte-1ipelgc {{ display: none !important; }}

        /* Modal overlay styling - only when visible */
        .{CSSClasses.MODAL_VISIBLE} {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background-color: rgba(0, 0, 0, 0.7) !important;
            z-index: 9999 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        /* Modal content styling - only when modal is visible */
        .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.MODAL_CONTENT} {{
            background: #131313  !important;
            border-radius: 15px !important;
            padding: 1.8rem !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
            max-width: min(500px, 90vw) !important;
            width: 90% !important;
            max-height: 80vh !important;
            overflow-y: auto !important;
            position: relative !important;
            z-index: 10000 !important;
        }}

        /* Modal header styling with responsive fonts */
        .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.MODAL_CONTENT} h2 {{
            color: white !important;
            text-align: center !important;
            margin-bottom: 1.2rem !important;
            font-size: 1.4rem !important;
        }}

        /* Modal text styling with responsive fonts */
        .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.MODAL_CONTENT} p {{
            color: white !important;
            text-align: center !important;
            margin-bottom: 1.2rem !important;
            line-height: 1.6 !important;
            font-size: 1rem !important;
        }}

        /* Responsive modal text for smaller screens */
        @media screen and (max-width: 768px) {{
            .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.MODAL_CONTENT} {{
                padding: 1.2rem !important;
            }}
            
            .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.MODAL_CONTENT} h2 {{
                font-size: 1.2rem !important;
                margin-bottom: 1rem !important;
            }}
            
            .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.MODAL_CONTENT} p {{
                font-size: 0.9rem !important;
                margin-bottom: 1rem !important;
            }}
        }}

        /* Attempts display styling */
        .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.ATTEMPTS_DISPLAY} {{
            background: #131313 !important;
            border: 2px solid #131313 !important;
            border-radius: 10px !important;
            padding: 1rem !important;
            margin: 1.2rem 0 !important;
            text-align: center !important;
        }}

        .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.ATTEMPTS_DISPLAY} strong {{
            color: #e74c3c !important;
            font-size: 1.1rem !important;
        }}

        /* Modal buttons container */
        .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.MODAL_BUTTONS} {{
            display: flex !important;
            gap: 1rem !important;
            justify-content: center !important;
            margin-top: 1.5rem !important;
            flex-wrap: wrap !important;
        }}

        /* Modal buttons styling with responsive sizing */
        .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.MODAL_BUTTONS} button {{
            padding: 0.8rem 1.5rem !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            font-size: 0.95rem !important;
            border: none !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            min-width: 140px !important;
            flex: 1 !important;
            max-width: 200px !important;
        }}

        @media screen and (max-width: 768px) {{
            .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.MODAL_BUTTONS} {{
                flex-direction: column !important;
                gap: 0.8rem !important;
            }}
            
            .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.MODAL_BUTTONS} button {{
                padding: 0.7rem 1.2rem !important;
                font-size: 0.85rem !important;
                min-width: auto !important;
                max-width: none !important;
            }}
        }}

        .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.CONFIRM_SOLVE_BTN} {{
            background: #27ae60 !important;
            color: white !important;
        }}

        .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.CONFIRM_SOLVE_BTN}:hover {{
            background: #219a52 !important;
            transform: translateY(-2px) !important;
        }}

        .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.CANCEL_SOLVE_BTN} {{
            background: #95a5a6 !important;
            color: white !important;
        }}

        .{CSSClasses.MODAL_VISIBLE} #{CSSClasses.CANCEL_SOLVE_BTN}:hover {{
            background: #7f8c8d !important;
            transform: translateY(-2px) !important;
        }}

        /* Warning styling for last attempt */
        .{CSSClasses.MODAL_VISIBLE} .{CSSClasses.LAST_ATTEMPT_WARNING} {{
            background: #fff3cd !important;
            border: 2px solid #ffeaa7 !important;
            color: #856404 !important;
            border-radius: 10px !important;
            padding: 1rem !important;
            margin: 1rem 0 !important;
            text-align: center !important;
            font-weight: bold !important;
            font-size: 0.9rem !important;
        }}

        /* Settings modal with responsive sizing */
        #settings-modal {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background-color: rgba(0, 0, 0, 0.8) !important;
            z-index: 9999 !important;
            display: none !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        #settings-modal.modal-visible {{
            display: flex !important;
        }}

        #settings-modal-content {{
            background: #1a1a1a !important;
            border-radius: 15px !important;
            padding: 1.8rem !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
            max-width: min(50vw, 90vw) !important;
            width: 90% !important;
            max-height: 90vh !important;
            overflow-y: auto !important;
            position: relative !important;
            border: 2px solid #333 !important;
            flex-direction: row;
            display: flex;
        }}

        #settings-modal-content h2 {{
            color: white !important;
            text-align: center !important;
            margin-bottom: 1.5rem !important;
            font-size: 1.6rem !important;
        }}

        #settings-modal-content h3 {{
            color: #4CAF50 !important;
            margin-top: 1.5rem !important;
            margin-bottom: 1rem !important;
            font-size: 1.2rem !important;
        }}

        #settings-modal-content p {{
            color: #ccc !important;
            line-height: 1.6 !important;
            margin-bottom: 1rem !important;
            font-size: 1rem !important;
        }}

        /* Responsive settings modal for smaller screens */
        @media screen and (max-width: 768px) {{
            #settings-modal-content {{
                padding: 1.2rem !important;
            }}
            
            #settings-modal-content h2 {{
                font-size: 1.4rem !important;
                margin-bottom: 1.2rem !important;
            }}
            
            #settings-modal-content h3 {{
                font-size: 1.1rem !important;
                margin-top: 1.2rem !important;
                margin-bottom: 0.8rem !important;
            }}
            
            #settings-modal-content p {{
                font-size: 0.9rem !important;
                margin-bottom: 0.8rem !important;
            }}
        }}

        #language-dropdown {{
            margin-bottom: 1rem !important;
        }}

        #language-status {{
            background: #2a2a2a !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            margin: 1rem 0 !important;
            border-left: 4px solid #4CAF50 !important;
            font-size: 0.95rem !important;
        }}

        #language-status strong {{
            color: #4CAF50 !important;
        }}

        #settings-modal-buttons {{
            display: flex !important;
            gap: 1rem !important;
            justify-content: center !important;
            margin-top: 1.8rem !important;
            flex-wrap: wrap !important;
        }}

        #settings-modal-buttons button {{
            padding: 0.8rem 1.5rem !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            font-size: 0.95rem !important;
            border: none !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            min-width: 140px !important;
            flex: 1 !important;
            max-width: 200px !important;
        }}

        @media screen and (max-width: 768px) {{
            #settings-modal-buttons {{
                flex-direction: column !important;
                gap: 0.8rem !important;
            }}
            
            #settings-modal-buttons button {{
                padding: 0.7rem 1.2rem !important;
                font-size: 0.85rem !important;
                min-width: auto !important;
                max-width: none !important;
            }}
        }}

        #settings-apply-btn {{
            background: #4CAF50 !important;
            color: white !important;
        }}

        #settings-apply-btn:hover {{
            background: #45a049 !important;
            transform: translateY(-2px) !important;
        }}

        #settings-close-btn {{
            background: #95a5a6 !important;
            color: white !important;
        }}

        #settings-close-btn:hover {{
            background: #7f8c8d !important;
            transform: translateY(-2px) !important;
        }}
        
        /* Save/Load section styling in settings modal */
        #settings-modal-content h4 {{
            color: #4CAF50 !important;
            margin-bottom: 0.8rem !important;
            font-size: 1rem !important;
            font-weight: bold !important;
        }}

        /* Save button styling */
        #settings-modal-content .save-game-button {{
            background: linear-gradient(135deg, #4CAF50, #45a049) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1rem !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3) !important;
        }}

        #settings-modal-content .save-game-button:hover {{
            background: linear-gradient(135deg, #45a049, #3d8b40) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4) !important;
        }}

        /* Load button styling */
        #settings-modal-content .load-game-button {{
            background: linear-gradient(135deg, #2196F3, #1976D2) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1rem !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 8px rgba(33, 150, 243, 0.3) !important;
        }}

        #settings-modal-content .load-game-button:hover:not(:disabled) {{
            background: linear-gradient(135deg, #1976D2, #1565C0) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(33, 150, 243, 0.4) !important;
        }}

        #settings-modal-content .load-game-button:disabled {{
            background: #666 !important;
            color: #999 !important;
            cursor: not-allowed !important;
            transform: none !important;
            box-shadow: none !important;
        }}

        /* File upload styling */
        #settings-modal-content .file-upload {{
            border: 2px dashed #4CAF50 !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            background: rgba(76, 175, 80, 0.1) !important;
            transition: all 0.3s ease !important;
        }}

        #settings-modal-content .file-upload:hover {{
            border-color: #45a049 !important;
            background: rgba(76, 175, 80, 0.15) !important;
        }}

        /* Save/Load status display */
        #save-load-status {{
            background: #2a2a2a !important;
            border-radius: 8px !important;
            padding: 1rem !important;
            margin: 1rem 0 !important;
            border-left: 4px solid #4CAF50 !important;
            font-size: 0.9rem !important;
            line-height: 1.4 !important;
        }}

        #save-load-status strong {{
            color: #4CAF50 !important;
        }}

        /* Success status */
        #save-load-status:has-text("✅") {{
            border-left-color: #4CAF50 !important;
            background: rgba(76, 175, 80, 0.1) !important;
        }}

        /* Error status */
        #save-load-status:has-text("❌") {{
            border-left-color: #f44336 !important;
            background: rgba(244, 67, 54, 0.1) !important;
        }}

        #save-load-status:has-text("❌") strong {{
            color: #f44336 !important;
        }}

        /* Save/Load section divider */
        #settings-modal-content .save-load-section {{
            border-top: 1px solid #444 !important;
            margin-top: 1.5rem !important;
            padding-top: 1.5rem !important;
        }}

        /* Responsive adjustments for save/load */
        @media screen and (max-width: 768px) {{
            #settings-modal-content .save-load-buttons {{
                flex-direction: column !important;
                gap: 1rem !important;
            }}
            
            #settings-modal-content .save-game-button,
            #settings-modal-content .load-game-button {{
                width: 100% !important;
                padding: 0.8rem !important;
            }}
            
            #save-load-status {{
                font-size: 0.8rem !important;
                padding: 0.8rem !important;
            }}
        }}

        .message-buttons-left{{
            display: none;
        }}


"""