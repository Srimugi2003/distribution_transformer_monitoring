import streamlit as st
import pickle
import numpy as np
model=pickle.load(open('monitor1.pkl','rb'))

oil_level_threshold = 70
oil_temp_threshold = 35
winding_temp_threshold = 45
oil_level_feature_index = 0
oil_temp_feature_index = 1
winding_temp_feature_index = 2

tree = model.tree_

def find_threshold(oil_level_threshold, oil_temp_threshold, winding_temp_threshold):
    def traverse(node):
        if tree.feature[node] == oil_level_feature_index:
            if tree.threshold[node] > oil_level_threshold:
                return True  # Oil level above threshold indicates fault
            else:
                if tree.children_left[node] != tree.children_right[node]:
                    return traverse(tree.children_left[node]) or traverse(tree.children_right[node])
                else:
                    return False  # Oil level below threshold indicates safe
        elif tree.feature[node] == oil_temp_feature_index:
            if tree.threshold[node] > oil_temp_threshold:
                return True  # Oil temperature above threshold indicates fault
            else:
                if tree.children_left[node] != tree.children_right[node]:
                    return traverse(tree.children_left[node]) or traverse(tree.children_right[node])
                else:
                    return False  # Oil temperature below threshold indicates safe
        elif tree.feature[node] == winding_temp_feature_index:
            if tree.threshold[node] > winding_temp_threshold:
                return True  # Winding temperature above threshold indicates fault
            else:
                if tree.children_left[node] != tree.children_right[node]:
                    return traverse(tree.children_left[node]) or traverse(tree.children_right[node])
                else:
                    return False  # Winding temperature below threshold indicates safe
        else:
            if tree.children_left[node] != tree.children_right[node]:
                return traverse(tree.children_left[node]) or traverse(tree.children_right[node])
            else:
                return False  # Default: return False if no condition is met
    
    return traverse(0)
oil_level_greater_than_threshold = find_threshold(oil_level_feature_index, oil_level_threshold, winding_temp_threshold)
oil_temp_greater_than_threshold = find_threshold(oil_temp_feature_index, oil_temp_threshold, oil_level_threshold)
winding_temp_greater_than_threshold = find_threshold(winding_temp_feature_index, winding_temp_threshold, oil_temp_threshold)

print("Oil level greater than threshold:", oil_level_greater_than_threshold)
print("Oil temperature greater than threshold:", oil_temp_greater_than_threshold)
print("Winding temperature greater than threshold:", winding_temp_greater_than_threshold)

def main():
    st.title("TRANSFORMER MONITORING")
    html_level = """
    <div style="background-color:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">TRANSFORMER MONITORING ML App </h2>
    </div>
    """
    st.markdown(html_level, unsafe_allow_html=True)

    OIL_LEVEL = st.text_input("OIL LEVEL","%")
    OIL_TEMP = st.text_input("OIL TEMP","deg C")
    WINDING_TEMP = st.text_input("WINDING TEMP","deg C")

    safe_html="""  
      <div style="background-color:#F4D03F;padding:10px >
       <h2 style="color:white;text-align:center;"> Your transformer is safe</h2>
       </div>
    """
    danger_html="""  
      <div style="background-color:#F08080;padding:10px >
       <h2 style="color:black ;text-align:center;"> Your transformer is in danger</h2>
       </div>
    """
    def find_fault_oillevel(OIL_LEVEL_str):
       OIL_LEVEL= float(OIL_LEVEL_str)
       if OIL_LEVEL > 70 :
        return "Faulty"
       else:
        return "Safe"
    def find_fault_oiltemp(OIL_TEMP_str):
       OIL_TEMP= float(OIL_TEMP_str)
       if OIL_TEMP > 35 :
        return "Faulty"
       else:
        return "Safe"
    def find_fault_windingtemp(WINDING_TEMP_str):
       WINDING_TEMP= float(WINDING_TEMP_str)
       if WINDING_TEMP > 45 :
        return "Faulty"
       else:
        return "Safe"
    if st.button("Predict oil level"):
        output=find_fault_oillevel(OIL_LEVEL)
        if output=="Faulty":
            st.success("The oil level is high")
            st.markdown(danger_html,unsafe_allow_html=True)
        else:
            st.markdown(safe_html,unsafe_allow_html=True)
    if st.button("Predict oil temp"):
        output=find_fault_oiltemp(OIL_TEMP)
        if output=="Faulty":
            st.success("The oil temp is high")
            st.markdown(danger_html,unsafe_allow_html=True)
        else:
            st.markdown(safe_html,unsafe_allow_html=True)
    if st.button("Predict winding temp"):
        output=find_fault_windingtemp(WINDING_TEMP)
        if output=="Faulty":
            st.success("The winding temp is high")
            st.markdown(danger_html,unsafe_allow_html=True)
        else:
            st.markdown(safe_html,unsafe_allow_html=True)       

if __name__=='__main__':
    main()
