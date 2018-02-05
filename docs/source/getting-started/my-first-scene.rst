********************
My first 3D scene
********************

Download the example: `material file <https://raw.githubusercontent.com/UmSenhorQualquer/py3dsceneeditor/refactoring/docs/_static/my-first-scene/teste.mtl>`_, `object file <https://raw.githubusercontent.com/UmSenhorQualquer/py3dsceneeditor/refactoring/docs/_static/my-first-scene/teste.obj>`_

.. code-block:: python

    from py3dengine.utils.WavefrontOBJFormat.WavefrontOBJReader import WavefrontOBJReader
    from py3dengine.scenes.GLScene import GLScene
    from py3dengine.bin.RunScene import RunScene


    w = WavefrontOBJReader('DolphinScene.obj')

    scene = GLScene()
    scene.objects = w.objects
    scene.cameras = w.cameras

    camera = scene.getCamera('Camera1')

    ray     = camera1.addRay( 100, 100 )
    x, y, z = ray.collidePlanZ(0); 

    floor   = scene.getObject('Floor')
    collision = ray.collide([floor])


    run = RunScene(scene)
    run.startScene()