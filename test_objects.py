import os
import os.path as osp
import json

def loadObjProposals(bboxDir):
    objProposals = {}
    obj2viewpoint = {}
    for efile in os.listdir(bboxDir):
        if efile.endswith('.json'):
            with open(osp.join(bboxDir,efile)) as f:
                scan = efile.split('_')[0]
                scanvp, _ = efile.split('.')
                data = json.load(f)
                for vp, vv in data.items():
                    for objid, objinfo in vv.items():
                        if objinfo['visible_pos']:
                            if scan + '_' + objid in obj2viewpoint:
                                if vp not in obj2viewpoint[scan + '_' + objid]:
                                    obj2viewpoint[scan + '_' + objid].append(vp)
                            else:
                                obj2viewpoint[scan + '_' + objid] = [vp, ]

                            if scanvp in objProposals:
                                for ii, bbox in enumerate(objinfo['bbox2d']):
                                    objProposals[scanvp]['bbox'].append(bbox)
                                    objProposals[scanvp]['visible_pos'].append(objinfo['visible_pos'][ii])
                                    objProposals[scanvp]['objId'].append(objid)

                            else:
                                objProposals[scanvp] = {'bbox': objinfo['bbox2d'],
                                                        'visible_pos': objinfo['visible_pos']}
                                objProposals[scanvp]['objId'] = []
                                for _ in objinfo['visible_pos']:
                                    objProposals[scanvp]['objId'].append(objid)

    return objProposals, obj2viewpoint

bboxDir = 'tasks/REVERIE/data/BBox'
objProposals, obj2viewpoint = loadObjProposals(bboxDir)
print(objProposals)
